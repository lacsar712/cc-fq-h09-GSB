import { describe, it } from 'node:test'
import assert from 'node:assert/strict'

import { assertSubmittable, isBlankText } from '../src/utils/fastqValidate.js'

describe('isBlankText', () => {
  it('treats empty and whitespace-only as blank', () => {
    assert.equal(isBlankText(''), true)
    assert.equal(isBlankText('   '), true)
    assert.equal(isBlankText('\n\t \r'), true)
    assert.equal(isBlankText(null), true)
    assert.equal(isBlankText(undefined), true)
  })

  it('treats real content as non-blank', () => {
    assert.equal(isBlankText('@SEQ1\nACGT\n+\nIIII'), false)
  })
})

describe('assertSubmittable - paste path', () => {
  it('rejects empty paste', () => {
    assert.throws(() => assertSubmittable({ fastqText: '', sampleId: null }), /FASTQ/)
    assert.throws(() => assertSubmittable({ fastqText: '   \n  ', sampleId: null }))
    assert.throws(() => assertSubmittable({ fastqText: '', sampleId: undefined }))
  })

  it('accepts a legal paste so the run can start', () => {
    assert.equal(
      assertSubmittable({ fastqText: '@SEQ1\nACGT\n+\nIIII\n', sampleId: null }),
      true,
    )
  })
})

describe('assertSubmittable - sample path', () => {
  it('accepts a concrete selected sample (content is re-checked server-side)', () => {
    assert.equal(assertSubmittable({ fastqText: '', sampleId: 1 }), true)
  })

  it('does not treat 0 / null as "no path" inconsistently', () => {
    assert.throws(() => assertSubmittable({ fastqText: ' ', sampleId: null }))
    assert.equal(assertSubmittable({ fastqText: ' ', sampleId: 0 }), true)
  })
})
