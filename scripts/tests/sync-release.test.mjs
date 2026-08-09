import assert from 'node:assert/strict';
import test from 'node:test';

import { validateRelease } from '../sync-go-zero-release.mjs';


test('validateRelease accepts a complete semantic release', () => {
  const release = {
    tag_name: 'v1.10.3',
    html_url: 'https://github.com/zeromicro/go-zero/releases/tag/v1.10.3',
    published_at: '2026-08-01T00:00:00Z',
  };
  assert.equal(validateRelease(release), release);
});

test('validateRelease rejects null and incomplete metadata', () => {
  assert.throws(() => validateRelease({ tag_name: null }), /invalid release tag/);
  assert.throws(
    () => validateRelease({ tag_name: 'v1.10.3' }),
    /missing its URL or publication date/,
  );
});
