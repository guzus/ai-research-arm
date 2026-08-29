export class EvidenceContractError extends Error {
  constructor(message) {
    super(message);
    this.name = 'EvidenceContractError';
  }
}

export function assertClaimReuseContract(claim) {
  const article = typeof claim?.article === 'string' && claim.article ? claim.article : '<unknown-article>';
  const key = typeof claim?.key === 'string' && claim.key
    ? claim.key
    : `${article}#${claim?.id || '<unknown-claim>'}`;
  if (typeof claim?.reusable !== 'boolean') {
    throw new EvidenceContractError(`claim reuse contract: ${key}: reusable must be boolean`);
  }
  if (claim.reusable === false && (typeof claim.reuse_block !== 'string' || !claim.reuse_block.trim())) {
    throw new EvidenceContractError(`claim reuse contract: ${key}: reusable=false requires a non-empty reuse_block`);
  }
}
