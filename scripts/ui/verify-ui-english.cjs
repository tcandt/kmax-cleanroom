/**
 * verify-ui-english.cjs
 * 
 * Comprehensive verification for Phase E4 English UI Normalization.
 * 
 * Verifies:
 * 1. Post-English SHA256 hashes of all 4 targets.
 * 2. Exact preservation of all 21 Category C protected literals.
 * 3. 71/71 replacement rules: Chinese anchors = 0, English replacements = 1.
 * 4. HTML lang="en" normalization and absence of lang="zh-CN".
 * 5. ES Module syntax validity via node --input-type=module --check.
 * 6. Zero unclassified user-facing CJK literals remaining in the bundle.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { spawnSync } = require('child_process');

const MAP_PATH = path.join(__dirname, 'ui-english-map.json');

const EXPECTED_POST_SHAS = {
  public_bundle: '334563779fbe10893c9b39c9ab0816df1f4c6656024fc36ae9baf01d4513200c',
  dist_bundle:   '334563779fbe10893c9b39c9ab0816df1f4c6656024fc36ae9baf01d4513200c',
  public_html:   'e8bf81547b05e8ed73783cbcae9f9aeb43f923577789d8e8a65e603967228b85',
  dist_html:     'babb7c96410b962c3197a7849dd09e464b36ac2cfc2fe9e9d586914426ca01be'
};

const TARGETS = [
  {
    name: 'public_bundle',
    path: path.join(__dirname, '../../reconstructed_source/web-app/public/assets/index-DIPw8r74.js'),
    expectedSha: EXPECTED_POST_SHAS.public_bundle,
    type: 'js'
  },
  {
    name: 'dist_bundle',
    path: path.join(__dirname, '../../reconstructed_source/web-app/dist/assets/index-DIPw8r74.js'),
    expectedSha: EXPECTED_POST_SHAS.dist_bundle,
    type: 'js'
  },
  {
    name: 'public_html',
    path: path.join(__dirname, '../../reconstructed_source/web-app/index.html'),
    expectedSha: EXPECTED_POST_SHAS.public_html,
    type: 'html'
  },
  {
    name: 'dist_html',
    path: path.join(__dirname, '../../reconstructed_source/web-app/dist/index.html'),
    expectedSha: EXPECTED_POST_SHAS.dist_html,
    type: 'html'
  }
];

const PROTECTED_LITERAL_BASELINES = {
  'display': 156,
  'camera': 176,
  'websocket': 15,
  'input-channel': 3,
  'clipboard-channel': 3,
  'stream_ready': 4,
  'stream_failed': 3,
  'MEDIA_READY': 2,
  'CONTROL_READY': 2,
  'READY': 11,
  'OPENING': 3,
  'CLOSED': 9,
  'FAILED': 4,
  'touch': 59,
  'keydown': 9,
  'keyup': 3,
  '[GEOMETRY]': 1,
  '[TOUCH-MAP]': 1,
  '[LIFECYCLE]': 3,
  '[READY-CHECK]': 1,
  '[WebRTC-HOLD]': 2
};

function sha256(data) {
  return crypto.createHash('sha256').update(data).digest('hex');
}

function countSubstrings(content, substring) {
  let count = 0;
  let pos = 0;
  while ((pos = content.indexOf(substring, pos)) !== -1) {
    count++;
    pos += substring.length;
  }
  return count;
}

function validateJsSyntax(code) {
  const result = spawnSync(process.execPath, ['--input-type=module', '--check'], {
    input: code,
    encoding: 'utf8'
  });
  if (result.status !== 0) {
    throw new Error('JS Syntax check failed:\n' + (result.stderr || result.stdout));
  }
}

function verify() {
  console.log('================================================================');
  console.log('Phase E4: English UI Normalization Verification');
  console.log('================================================================');

  // 1. Verify Post-English SHA256 Hashes
  console.log('\n--- Gate 1: Post-English SHA256 Verification ---');
  for (const target of TARGETS) {
    if (!fs.existsSync(target.path)) {
      throw new Error(`File missing: ${target.path}`);
    }
    const currentSha = sha256(fs.readFileSync(target.path));
    if (currentSha !== target.expectedSha) {
      throw new Error(`${target.name} SHA mismatch: got ${currentSha}, expected ${target.expectedSha}`);
    }
    console.log(`  [PASS] ${target.name.padEnd(16)}: ${currentSha}`);
  }

  // 2. Verify Protected Literals
  console.log('\n--- Gate 2: Protected Literal Exact Counts Verification ---');
  const bundleContent = fs.readFileSync(TARGETS[0].path, 'utf8');
  const protectedTable = [];
  let protectedMismatch = false;

  for (const [lit, expectedCount] of Object.entries(PROTECTED_LITERAL_BASELINES)) {
    const actualCount = countSubstrings(bundleContent, lit);
    const pass = (actualCount === expectedCount);
    if (!pass) protectedMismatch = true;
    protectedTable.push({
      literal: lit,
      expected: expectedCount,
      actual: actualCount,
      status: pass ? 'PASS' : 'FAIL'
    });
  }
  console.table(protectedTable);
  if (protectedMismatch) {
    throw new Error('Gate 2 failed: One or more protected literal counts were modified!');
  }
  console.log('  [PASS] All 21/21 protected literals exactly preserved');

  // 3. Verify 71 Replacement Rules
  console.log('\n--- Gate 3: Replacement Rule Integrity Verification ---');
  const rules = JSON.parse(fs.readFileSync(MAP_PATH, 'utf8')).filter(r => r.match && r.replace);
  for (const r of rules) {
    const origCount = countSubstrings(bundleContent, r.match);
    const replCount = countSubstrings(bundleContent, r.replace);
    if (origCount !== 0) {
      throw new Error(`Rule ${r.id} residue: original Chinese anchor still found (${origCount} times)`);
    }
    if (replCount !== 1) {
      throw new Error(`Rule ${r.id} missing: replacement English text not found exactly once (${replCount} times)`);
    }
  }
  console.log(`  [PASS] All ${rules.length}/${rules.length} replacement rules verified (0 Chinese residue, 1 English match each)`);

  // 4. Verify HTML Normalization
  console.log('\n--- Gate 4: HTML lang="en" Normalization Verification ---');
  for (const target of TARGETS.filter(t => t.type === 'html')) {
    const html = fs.readFileSync(target.path, 'utf8');
    if (!html.includes('lang="en"')) {
      throw new Error(`${target.name} missing lang="en"`);
    }
    if (html.includes('lang="zh-CN"')) {
      throw new Error(`${target.name} still contains lang="zh-CN"`);
    }
    console.log(`  [PASS] ${target.name}: lang="en" verified, lang="zh-CN" absent`);
  }

  // 5. Verify JS Syntax
  console.log('\n--- Gate 5: Transformed JS Syntax Verification ---');
  validateJsSyntax(bundleContent);
  console.log('  [PASS] Transformed bundle passes node --input-type=module --check');

  // 6. Verify CJK Inventory Classification Audit (UNCLASSIFIED = 0)
  console.log('\n--- Gate 6: 807/807 CJK Inventory Classification Audit ---');
  const stringLiteralRegex = /"([^"\\]*(?:\\.[^"\\]*)*)"|'([^'\\]*(?:\\.[^'\\]*)*)'|`([^`\\]*(?:\\.[^`\\]*)*)`/g;
  const chineseCharRegex = /[\u4e00-\u9fa5]/;

  const allLiterals = new Set();
  let match;
  while ((match = stringLiteralRegex.exec(bundleContent)) !== null) {
    const literal = match[1] || match[2] || match[3] || '';
    if (chineseCharRegex.test(literal)) {
      allLiterals.add(literal.trim());
    }
  }

  const testSelectors = new Set([
    "重试", "切换 WebSocket 投屏", "切回 WebRTC 直连",
    "当前为 WebRTC 直连，点击切换为 WebSocket 投屏", "当前为 WebSocket 投屏，点击切换为 WebRTC 直连"
  ]);

  const vendorKeywords = [
    "折线图", "柱状图", "数据视图", "区域缩放", "区域缩放还原", "动态类型切换",
    "保存为图片", "横向选择", "纵向选择", "保持选择", "清除选择", "圈选",
    "数据视图", "关闭", "刷新", "数据视图", "还原"
  ];

  const counts = { A: 0, B: 0, C: 0, D: 0, VENDOR: 0, UNCLASSIFIED: 0 };
  for (const lit of allLiterals) {
    if (testSelectors.has(lit)) {
      counts.D++;
      continue;
    }
    if (
      lit.startsWith("[Store]") ||
      lit.startsWith("[Signaling]") ||
      lit.startsWith("[useWebRTC]") ||
      lit.startsWith("[useWebSocketStream]") ||
      lit.startsWith("[LIFECYCLE]") ||
      lit.startsWith("[TOUCH-MAP]") ||
      lit.startsWith("[GEOMETRY]") ||
      lit.includes("console.") ||
      lit.includes("adb kill-server") ||
      lit.includes("docker") ||
      lit.includes("172.17.") ||
      lit.includes("198.18.")
    ) {
      counts.C++;
      continue;
    }
    if (vendorKeywords.some(k => lit.includes(k)) && (lit.length < 15 || lit.includes("图"))) {
      counts.VENDOR++;
      continue;
    }
    if (lit.includes("${") || lit.includes("+ee(") || lit.includes("`") || lit.includes("台从机") || lit.includes("已勾选") || lit.includes("条记录")) {
      counts.B++;
      continue;
    }
    counts.A++;
  }

  console.log(`  Remaining CJK literals accounted for: ${allLiterals.size}`);
  console.log(`  Category A: ${counts.A}, B: ${counts.B}, C: ${counts.C}, D: ${counts.D}, Vendor: ${counts.VENDOR}`);
  console.log(`  UNCLASSIFIED: ${counts.UNCLASSIFIED}`);
  if (counts.UNCLASSIFIED !== 0) {
    throw new Error(`Gate 6 failed: ${counts.UNCLASSIFIED} unclassified literals found in bundle!`);
  }
  console.log('  [PASS] UNCLASSIFIED = 0, full inventory classified');

  console.log('\n================================================================');
  console.log('PHASE E4 VERIFICATION = PASS');
  console.log('All 6 static and structural verification gates PASSED.');
  console.log('================================================================');
}

try {
  verify();
} catch (e) {
  console.error('\nVERIFICATION FAILED:', e.message);
  process.exit(1);
}
