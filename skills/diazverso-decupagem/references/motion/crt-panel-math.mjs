/** crt - safety/geometry for contextual CRT film/TV panels.
 * Pure module, no video fetching or media analysis.
 */
export function planCrtPanel(config) {
  if (!config || typeof config !== 'object') throw new Error('clip plan required');
  const {src, rightsStatus, evidence, startFrame, durationFrames,
    availableFrames, outputWidth, outputHeight, audioAllowed = false,
    audioVolume = 0, scanlineOpacity = 0.28} = config;
  if (rightsStatus !== 'APPROVED' || typeof evidence !== 'string' || !evidence.trim()) {
    throw new Error('Clip usage requires documented rights review/approval');
  }
  if (typeof src !== 'string' || !src.trim() || /^(?:https?:|file:|\/|\\|~)/i.test(src)
      || src.split(/[\\/]/).some(part => !part || part === '..' || part === '.')) {
    throw new Error('Only safe project-relative media paths');
  }
  for (const [name,n] of Object.entries({startFrame,durationFrames,availableFrames,outputWidth,outputHeight})) {
    if (!Number.isSafeInteger(n) || (name === 'startFrame' ? n < 0 : n <= 0)) throw new Error('Invalid '+name);
  }
  if (startFrame + durationFrames > availableFrames) throw new Error('Clip trim outside verified source duration');
  if (typeof audioAllowed !== 'boolean' || !Number.isFinite(audioVolume)
      || audioVolume < 0 || audioVolume > 1 || (!audioAllowed && audioVolume !== 0)) {
    throw new Error('Audio must be separately authorized and volume controlled');
  }
  if (!Number.isFinite(scanlineOpacity) || scanlineOpacity < 0.12 || scanlineOpacity > 0.55) {
    throw new Error('CRT scanline opacity must remain visible but bounded');
  }
  const margin = Math.max(20, Math.round(Math.min(outputWidth,outputHeight)*0.055));
  const width = outputWidth - 2*margin;
  const height = Math.min(outputHeight-2*margin, Math.round(width*9/16));
  if (width <= 0 || height <= 0) throw new Error('No usable panel area');
  return {src, startFrame, durationFrames, audioVolume:audioAllowed?audioVolume:0,
    scanlineOpacity, panel:{width,height,left:(outputWidth-width)/2,
      top:(outputHeight-height)/2}, rightsEvidence:evidence.trim(),
    runtimeVerified:false, rightsVerifiedByCode:false};
}
