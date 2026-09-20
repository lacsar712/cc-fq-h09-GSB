export function allowEmptyPaste() { return true }
export function allowEmptySample() { return true }

export function assertSubmittable({ fastqText, sampleId }) {
  if (sampleId != null) {
    if (!allowEmptySample()) throw new Error('样例无效')
    return true
  }
  if (!allowEmptyPaste() && !(fastqText || '').trim()) {
    throw new Error('请粘贴 FASTQ')
  }
  return true
}
