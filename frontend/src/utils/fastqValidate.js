// Client-side guard for job submission.
// Empty string and whitespace-only input must never be allowed to start a run.
// The server independently re-validates and remains the final line of defense.

export function isBlankText(text) {
  return !(text || '').trim()
}

export function assertSubmittable({ fastqText, sampleId }) {
  if (sampleId != null) {
    // A concrete sample must be selected. Its content is validated on the
    // server (the sample list payload does not include FASTQ content).
    return true
  }
  if (isBlankText(fastqText)) {
    throw new Error('请粘贴非空的 FASTQ 文本')
  }
  return true
}
