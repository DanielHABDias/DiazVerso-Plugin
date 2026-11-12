// Sintetiza os SFX do kit de motion (sem samples de terceiros) e, com --base, uma base rítmica de rascunho
// a 120 BPM. Uso: node build_motion_sfx.mjs <pasta-nova> [--base]. Não sobrescreve arquivos existentes.
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';

const RATE = 48000;
const target = process.argv[2];
if (!target) { console.error('Informe a pasta de saída'); process.exit(2); }
const out = new URL(`file://${path.resolve(target)}/`);
mkdirSync(out, { recursive: true });

let seed = 7;
const rand = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 2 ** 32 * 2 - 1; };
const buffer = seconds => new Float32Array(Math.round(seconds * RATE));
const env = (t, attack, decay) => (t < attack ? t / attack : Math.exp(-(t - attack) / decay));

function save(name, data, gain = 0.9) {
  let peak = 0; for (const v of data) peak = Math.max(peak, Math.abs(v));
  const scale = peak > 0 ? gain / peak : 1;
  const bytes = Buffer.alloc(44 + data.length * 2);
  bytes.write('RIFF', 0); bytes.writeUInt32LE(36 + data.length * 2, 4); bytes.write('WAVE', 8); bytes.write('fmt ', 12);
  bytes.writeUInt32LE(16, 16); bytes.writeUInt16LE(1, 20); bytes.writeUInt16LE(1, 22); bytes.writeUInt32LE(RATE, 24);
  bytes.writeUInt32LE(RATE * 2, 28); bytes.writeUInt16LE(2, 32); bytes.writeUInt16LE(16, 34); bytes.write('data', 36); bytes.writeUInt32LE(data.length * 2, 40);
  data.forEach((v, i) => bytes.writeInt16LE(Math.max(-32767, Math.min(32767, Math.round(v * scale * 32767))), 44 + i * 2));
  const file = new URL(`${name}.wav`, out);
  if (existsSync(file)) throw new Error(`Já existe: ${name}.wav`);
  writeFileSync(file, bytes);
}

// Filtro passa-baixa de um polo (suficiente para "abafar" ruído).
const lowpass = (data, cutoffAt) => { let y = 0; for (let i = 0; i < data.length; i += 1) { const c = cutoffAt(i / RATE); const a = 1 - Math.exp(-2 * Math.PI * c / RATE); y += a * (data[i] - y); data[i] = y; } return data; };

const sfx = {
  pop: () => { const d = buffer(0.12); let ph = 0; d.forEach((_, i) => { const t = i / RATE; ph += 2 * Math.PI * (900 - 5000 * t) / RATE; d[i] = Math.sin(ph) * env(t, 0.002, 0.025); }); return d; },
  tick: () => { const d = buffer(0.05); d.forEach((_, i) => { const t = i / RATE; d[i] = (Math.sin(2 * Math.PI * 3200 * t) * 0.6 + rand() * 0.4) * env(t, 0.0005, 0.008); }); return d; },
  type: () => { const d = buffer(0.07); d.forEach((_, i) => { const t = i / RATE; d[i] = (rand() * 0.7 + Math.sin(2 * Math.PI * 1800 * t) * 0.3) * env(t, 0.001, 0.012); }); return lowpass(d, () => 6000); },
  whoosh: () => { const d = buffer(0.45); d.forEach((_, i) => { const t = i / RATE; d[i] = rand() * Math.sin(Math.PI * t / 0.45) ** 2; }); return lowpass(d, t => 300 + 5000 * Math.sin(Math.PI * t / 0.45)); },
  swish: () => { const d = buffer(0.22); d.forEach((_, i) => { const t = i / RATE; d[i] = rand() * Math.sin(Math.PI * t / 0.22); }); return lowpass(d, t => 1500 + 9000 * t / 0.22); },
  impact: () => { const d = buffer(1.2); let ph = 0; d.forEach((_, i) => { const t = i / RATE; ph += 2 * Math.PI * (35 + 90 * Math.exp(-t * 18)) / RATE; d[i] = Math.sin(ph) * env(t, 0.002, 0.35) + rand() * env(t, 0.001, 0.05) * 0.5; }); return d; },
  sub: () => { const d = buffer(1.6); let ph = 0; d.forEach((_, i) => { const t = i / RATE; ph += 2 * Math.PI * (55 * Math.exp(-t * 0.6)) / RATE; d[i] = Math.tanh(Math.sin(ph) * 2) * env(t, 0.004, 0.6); }); return d; },
  glitch: () => { const d = buffer(0.35); let hold = 0; d.forEach((_, i) => { const t = i / RATE; if (i % 220 === 0) hold = rand(); d[i] = (Math.round(hold * 4) / 4) * (Math.floor(t * 40) % 2 ? 1 : 0.3) * env(t, 0.001, 0.15); }); return d; },
  riser: () => { const d = buffer(2.2); let ph = 0; d.forEach((_, i) => { const t = i / RATE; ph += 2 * Math.PI * (120 + 900 * (t / 2.2) ** 2) / RATE; d[i] = (Math.sin(ph) * 0.5 + rand() * 0.5 * (t / 2.2)) * (t / 2.2) ** 1.5; }); return lowpass(d, t => 400 + 8000 * (t / 2.2)); },
  ding: () => { const d = buffer(1.0); d.forEach((_, i) => { const t = i / RATE; d[i] = (Math.sin(2 * Math.PI * 1568 * t) + 0.5 * Math.sin(2 * Math.PI * 2352 * t) + 0.25 * Math.sin(2 * Math.PI * 3920 * t)) * env(t, 0.002, 0.25); }); return d; },
  error: () => { const d = buffer(0.4); d.forEach((_, i) => { const t = i / RATE; const f = t < 0.18 ? 220 : 165; d[i] = Math.sign(Math.sin(2 * Math.PI * f * t)) * 0.5 * env(t % 0.2, 0.003, 0.08); }); return lowpass(d, () => 2500); },
  camera: () => { const d = buffer(0.25); d.forEach((_, i) => { const t = i / RATE; d[i] = rand() * (env(t, 0.001, 0.01) + (t > 0.08 ? env(t - 0.08, 0.001, 0.02) : 0)); }); return lowpass(d, () => 7000); },
};
for (const [name, make] of Object.entries(sfx)) save(name, make(), name === 'sub' || name === 'impact' ? 0.95 : 0.8);

if (!process.argv.includes('--base')) { console.log(`SFX: ${Object.keys(sfx).join(', ')}`); process.exit(0); }
// Base rítmica de rascunho: 120 BPM (0,5 s por tempo). Seções em segundos combinam com o roteiro.
const BPM = 120; const beat = 60 / BPM; const total = 60;
const bed = buffer(total);
const add = (start, data, gain) => { const o = Math.round(start * RATE); for (let i = 0; i < data.length && o + i < bed.length; i += 1) bed[o + i] += data[i] * gain; };
const kick = (() => { const d = buffer(0.35); let ph = 0; d.forEach((_, i) => { const t = i / RATE; ph += 2 * Math.PI * (48 + 140 * Math.exp(-t * 30)) / RATE; d[i] = Math.sin(ph) * env(t, 0.001, 0.12); }); return d; })();
const clap = (() => { const d = buffer(0.2); d.forEach((_, i) => { const t = i / RATE; d[i] = rand() * (env(t, 0.001, 0.05) + 0.5 * env(Math.max(0, t - 0.012), 0.001, 0.04)); }); return lowpass(d, () => 4500); })();
const hat = (() => { const d = buffer(0.06); d.forEach((_, i) => { const t = i / RATE; d[i] = rand() * env(t, 0.0005, 0.012); }); return d; })();
const notes = [55, 55, 65.41, 49]; // A1, A1, C2, G1 (lá menor)
const bass = freq => { const d = buffer(beat * 2); let ph = 0; d.forEach((_, i) => { const t = i / RATE; ph += freq / RATE; d[i] = ((ph % 1) * 2 - 1) * env(t, 0.005, 0.35); }); return lowpass(d, t => 250 + 900 * Math.exp(-t * 6)); };
const pad = (freq, seconds) => { const d = buffer(seconds); d.forEach((_, i) => { const t = i / RATE; d[i] = [1, 1.2, 1.5, 2].reduce((sum, ratio, k) => sum + Math.sin(2 * Math.PI * freq * ratio * t + k) / (k + 1), 0) * Math.min(1, t / 0.8, (seconds - t) / 0.8); }); return lowpass(d, () => 1200); };
const section = t => (t < 3 ? 'intro' : t < 14 ? 'beat' : t < 17 ? 'break' : t < 48 ? 'drop' : t < 55 ? 'half' : 'out');
for (let bar = 0; bar * beat * 4 < total; bar += 1) {
  const barStart = bar * beat * 4; const chord = notes[bar % 4];
  add(barStart, pad(chord * 4, beat * 4), section(barStart) === 'out' ? 0.05 : 0.07);
  for (let step = 0; step < 8; step += 1) {
    const t = barStart + step * beat / 2; const kind = section(t);
    if (kind === 'intro' || kind === 'break' || kind === 'out') continue;
    if (step % 2 === 0 && (step / 2) % 2 === 0) add(t, kick, 0.9);
    if (kind === 'drop' && step === 7) add(t, kick, 0.6);
    if (step % 4 === 2 && kind !== 'half') add(t, clap, 0.35);
    add(t, hat, step % 2 ? 0.12 : 0.2);
    if (step % 4 === 0 && kind !== 'half') add(t, bass(chord), 0.45);
  }
}
save('base-ritmica', bed, 0.7);
console.log(`SFX: ${Object.keys(sfx).join(', ')} + base-ritmica (${total} s, ${BPM} BPM)`);
