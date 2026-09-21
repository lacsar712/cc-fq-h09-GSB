import test from 'node:test'
import assert from 'node:assert/strict'

import { assertSubmittable, isBlank } from '../src/utils/fastqValidate.js'

test('isBlank covers null / empty / whitespace', () => {
  for (const v of [null, undefined, '', '   ', '\n\t \r\n']) {
    assert.equal(isBlank(v), true)
  }
  assert.equal(isBlank('@r1\nACGT\n+\nIIII\n'), false)
})

test('paste path: empty and whitespace-only text cannot start', () => {
  for (const fastqText of ['', '   ', '\n\t ']) {
    assert.throws(
      () => assertSubmittable({ fastqText, sampleId: null }),
      /FASTQ|粘贴/,
    )
  }
})

test('paste path: neither sample nor text cannot start', () => {
  assert.throws(() => assertSubmittable({ sampleId: null }), /粘贴/)
})

test('paste path: legal FASTQ text can start', () => {
  assert.equal(
    assertSubmittable({ fastqText: '@r1\nACGT\n+\nIIII\n', sampleId: null }),
    true,
  )
})

test('sample path: qualified sample (has_content) can start', () => {
  assert.equal(
    assertSubmittable({ sampleId: 1, sampleHasContent: true }),
    true,
  )
})

test('sample path: empty sample cannot start even if selected', () => {
  assert.throws(
    () => assertSubmittable({ sampleId: 2, sampleHasContent: false }),
    /样例内容为空/,
  )
})

test('sample path: missing content flag fails closed (client bypass attempt)', () => {
  assert.throws(() => assertSubmittable({ sampleId: 3 }), /样例/)
})
