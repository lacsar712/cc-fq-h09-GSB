export function isBlank(text) {
  return !(text || '').trim()
}

/**
 * Client-side guard before POST /api/jobs.
 * - sample path: a sample must be selected and have non-blank content
 * - paste path: pasted FASTQ must be non-blank
 * Throws Error with a user-facing message; the server remains the final gate.
 */
export function assertSubmittable({ fastqText, sampleId, sampleHasContent }) {
  if (sampleId != null) {
    if (sampleHasContent !== true) {
      throw new Error('样例内容为空,无法开跑')
    }
    return true
  }
  if (isBlank(fastqText)) {
    throw new Error('请粘贴非空的 FASTQ 文本')
  }
  return true
}
