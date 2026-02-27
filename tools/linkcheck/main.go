// linkcheck crawls https://go-zero.dev and reports broken internal links.
//
// Usage:
//
//	go run main.go                          # default: 2 req/s, 10 concurrent
//	go run main.go -rps 5 -concurrency 20  # faster
//	go run main.go -timeout 15s            # per-request timeout
package main

import (
	"context"
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"os"
	"sort"
	"strings"
	"sync"
	"time"

	"golang.org/x/net/html"
	"golang.org/x/time/rate"
)

// result holds the check outcome for a single URL.
type result struct {
	URL        string
	StatusCode int
	Err        error
	FoundOn    []string // pages where this URL was linked
}

func main() {
	var (
		baseURL     string
		rps         float64
		concurrency int
		timeout     time.Duration
		verbose     bool
	)

	flag.StringVar(&baseURL, "url", "https://go-zero.dev", "site root URL to crawl")
	flag.Float64Var(&rps, "rps", 2, "max requests per second (rate limit)")
	flag.IntVar(&concurrency, "concurrency", 10, "max concurrent requests")
	flag.DurationVar(&timeout, "timeout", 10*time.Second, "per-request timeout")
	flag.BoolVar(&verbose, "v", false, "verbose: print every checked URL")
	flag.Parse()

	base, err := url.Parse(baseURL)
	if err != nil {
		log.Fatalf("invalid base URL: %v", err)
	}

	c := &crawler{
		base:    base,
		client:  &http.Client{Timeout: timeout},
		limiter: rate.NewLimiter(rate.Limit(rps), max(1, int(rps))),
		sem:     make(chan struct{}, concurrency),
		visited: make(map[string]bool),
		results: make(map[string]*result),
		verbose: verbose,
	}

	fmt.Printf("🔍 Crawling %s (rps=%.0f, concurrency=%d, timeout=%s)\n\n",
		baseURL, rps, concurrency, timeout)

	start := time.Now()
	c.crawl(base.String(), "(root)")
	c.wg.Wait()
	elapsed := time.Since(start)

	// Collect and report broken links.
	var broken []*result
	for _, r := range c.results {
		if r.Err != nil || (r.StatusCode >= 400) {
			broken = append(broken, r)
		}
	}

	sort.Slice(broken, func(i, j int) bool {
		return broken[i].URL < broken[j].URL
	})

	fmt.Println()
	fmt.Println(strings.Repeat("─", 72))

	if len(broken) == 0 {
		fmt.Printf("✅ All %d internal links are healthy. (%s)\n", len(c.results), elapsed.Round(time.Millisecond))
		os.Exit(0)
	}

	fmt.Printf("❌ Found %d broken link(s) out of %d checked. (%s)\n\n",
		len(broken), len(c.results), elapsed.Round(time.Millisecond))

	for _, r := range broken {
		status := fmt.Sprintf("HTTP %d", r.StatusCode)
		if r.Err != nil {
			status = r.Err.Error()
		}
		fmt.Printf("  %s\n    Status: %s\n", r.URL, status)
		for _, page := range r.FoundOn {
			fmt.Printf("    Found on: %s\n", page)
		}
		fmt.Println()
	}

	os.Exit(1)
}

// crawler holds shared state for the concurrent link checker.
type crawler struct {
	base    *url.URL
	client  *http.Client
	limiter *rate.Limiter
	sem     chan struct{}
	wg      sync.WaitGroup

	mu      sync.Mutex
	visited map[string]bool
	results map[string]*result

	checked int
	verbose bool
}

// crawl fetches a page, extracts links, and recursively crawls internal ones.
func (c *crawler) crawl(rawURL, foundOn string) {
	normalized := c.normalize(rawURL)
	if normalized == "" {
		return
	}

	c.mu.Lock()
	if c.visited[normalized] {
		// Already queued — just record the back-reference.
		if r, ok := c.results[normalized]; ok {
			r.FoundOn = append(r.FoundOn, foundOn)
		}
		c.mu.Unlock()
		return
	}
	c.visited[normalized] = true
	c.results[normalized] = &result{URL: normalized, FoundOn: []string{foundOn}}
	c.mu.Unlock()

	c.wg.Add(1)
	go func() {
		defer c.wg.Done()

		// Acquire semaphore (concurrency limit).
		c.sem <- struct{}{}
		defer func() { <-c.sem }()

		// Rate limit.
		if err := c.limiter.Wait(context.Background()); err != nil {
			c.setErr(normalized, err)
			return
		}

		c.mu.Lock()
		c.checked++
		n := c.checked
		c.mu.Unlock()

		if c.verbose {
			fmt.Printf("  [%d] GET %s\n", n, normalized)
		} else if n%20 == 0 {
			fmt.Printf("  ... checked %d URLs so far\n", n)
		}

		resp, err := c.client.Get(normalized)
		if err != nil {
			c.setErr(normalized, err)
			return
		}
		defer resp.Body.Close()

		c.mu.Lock()
		c.results[normalized].StatusCode = resp.StatusCode
		c.mu.Unlock()

		// Only parse HTML pages for more links.
		ct := resp.Header.Get("Content-Type")
		if resp.StatusCode == http.StatusOK && strings.Contains(ct, "text/html") {
			// Use the final URL after redirects for resolving relative links.
			// e.g. /foo redirects to /foo/ — relative links must resolve from /foo/.
			finalURL := resp.Request.URL.String()
			links := extractLinks(resp.Body)
			for _, link := range links {
				resolved := c.resolve(finalURL, link)
				if resolved != "" && c.isInternal(resolved) {
					c.crawl(resolved, normalized)
				}
			}
		}
	}()
}

// normalize strips fragment and query, returns empty string for non-internal URLs.
func (c *crawler) normalize(rawURL string) string {
	u, err := url.Parse(rawURL)
	if err != nil {
		return ""
	}
	if !c.isInternalURL(u) {
		return ""
	}
	u.Fragment = ""
	u.RawQuery = ""
	// Ensure trailing slash consistency for directory-like paths.
	path := u.Path
	if path == "" {
		path = "/"
	}
	u.Path = path
	return u.String()
}

// resolve resolves a relative or absolute link against the page URL.
func (c *crawler) resolve(pageURL, href string) string {
	base, err := url.Parse(pageURL)
	if err != nil {
		return ""
	}
	ref, err := url.Parse(href)
	if err != nil {
		return ""
	}
	return base.ResolveReference(ref).String()
}

// isInternal checks if a fully resolved URL string belongs to the target site.
func (c *crawler) isInternal(rawURL string) bool {
	u, err := url.Parse(rawURL)
	if err != nil {
		return false
	}
	return c.isInternalURL(u)
}

func (c *crawler) isInternalURL(u *url.URL) bool {
	if u.Scheme != "" && u.Scheme != "http" && u.Scheme != "https" {
		return false
	}
	if u.Host != "" && u.Host != c.base.Host {
		return false
	}
	return true
}

func (c *crawler) setErr(normalized string, err error) {
	c.mu.Lock()
	defer c.mu.Unlock()
	if r, ok := c.results[normalized]; ok {
		r.Err = err
	}
}

// extractLinks parses HTML and returns all href values from <a> tags.
func extractLinks(r io.Reader) []string {
	var links []string
	tokenizer := html.NewTokenizer(r)
	for {
		tt := tokenizer.Next()
		switch tt {
		case html.ErrorToken:
			return links
		case html.StartTagToken, html.SelfClosingTagToken:
			t := tokenizer.Token()
			if t.Data != "a" {
				continue
			}
			for _, attr := range t.Attr {
				if attr.Key == "href" {
					href := strings.TrimSpace(attr.Val)
					if href != "" && !strings.HasPrefix(href, "javascript:") && !strings.HasPrefix(href, "mailto:") {
						links = append(links, href)
					}
				}
			}
		}
	}
}
