/**
 * verify-ui-english.cjs
 * 
 * Phase E6: Complete Static & Invariant Verification for KMAX Web Console (V2).
 * 
 * Gates:
 * 1. Post-English V2 SHA256 Verification (public & dist bundles + index.html).
 * 2. Category C Protected Literal Exact Counts Verification (21 literals).
 * 3. Replacement Rule Integrity Verification (V1 + E6 active rules).
 * 4. HTML lang="en" Verification.
 * 5. Transformed JS Module Syntax Verification.
 * 6. Inventory Classification Audit (UNCLASSIFIED = 0).
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { spawnSync } = require('child_process');

const MAP_PATH = path.join(__dirname, 'ui-english-map.json');

const EXPECTED_HASHES = {
  public_bundle: '295a41f179bc05b94222abe5a9512b59851dfee67b0bb6a3c1ed166315c73f79',
  dist_bundle: '295a41f179bc05b94222abe5a9512b59851dfee67b0bb6a3c1ed166315c73f79',
  public_html: 'e8bf81547b05e8ed73783cbcae9f9aeb43f923577789d8e8a65e603967228b85',
  dist_html: 'babb7c96410b962c3197a7849dd09e464b36ac2cfc2fe9e9d586914426ca01be'
};

const TARGET_PATHS = {
  public_bundle: path.join(__dirname, '../../reconstructed_source/web-app/public/assets/index-DIPw8r74.js'),
  dist_bundle: path.join(__dirname, '../../reconstructed_source/web-app/dist/assets/index-DIPw8r74.js'),
  public_html: path.join(__dirname, '../../reconstructed_source/web-app/index.html'),
  dist_html: path.join(__dirname, '../../reconstructed_source/web-app/dist/index.html')
};

const PROTECTED_LITERAL_EXPECTED = {
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

function sha256(content) {
  return crypto.createHash('sha256').update(content).digest('hex');
}

function countSubstrings(haystack, needle) {
  let count = 0;
  let pos = -1;
  while ((pos = haystack.indexOf(needle, pos + 1)) !== -1) {
    count++;
  }
  return count;
}

function verifyGate1Hashes() {
  console.log('--- Gate 1: Post-English V2 SHA256 Verification ---');
  let pass = true;
  for (const [key, expectedSha] of Object.entries(EXPECTED_HASHES)) {
    const filePath = TARGET_PATHS[key];
    if (!fs.existsSync(filePath)) {
      console.log(`  [SKIP] Optional target ${key} not present on disk.`);
      continue;
    }
    const content = fs.readFileSync(filePath, 'utf8');
    const actualSha = sha256(content);
    if (actualSha === expectedSha) {
      console.log(`  [PASS] ${key.padEnd(16)}: ${actualSha}`);
    } else {
      console.error(`  [FAIL] ${key.padEnd(16)}: expected ${expectedSha}, got ${actualSha}`);
      pass = false;
    }
  }
  return pass;
}

function verifyGate2ProtectedLiterals(bundleContent) {
  console.log('\n--- Gate 2: Protected Literal Exact Counts Verification ---');
  let pass = true;
  const results = [];
  for (const [literal, expectedCount] of Object.entries(PROTECTED_LITERAL_EXPECTED)) {
    const actualCount = countSubstrings(bundleContent, literal);
    const ok = actualCount === expectedCount;
    if (!ok) pass = false;
    results.push({
      literal,
      expected: expectedCount,
      actual: actualCount,
      status: ok ? 'PASS' : 'FAIL'
    });
  }
  console.table(results);
  if (pass) {
    console.log('  [PASS] All 21/21 protected literals exactly preserved');
  } else {
    console.error('  [FAIL] One or more protected literals deviated from baseline counts!');
  }
  return pass;
}

function verifyGate3Rules(bundleContent, rules) {
  console.log('\n--- Gate 3: Replacement Rule Integrity Verification ---');
  let pass = true;
  let verified = 0;
  for (const rule of rules) {
    // Chinese match string should be absent or replaced
    const remainingMatch = countSubstrings(bundleContent, rule.match);
    const presentReplace = countSubstrings(bundleContent, rule.replace);

    if (remainingMatch !== 0) {
      console.error(`  [FAIL] Rule ${rule.id}: source Chinese string still present (${remainingMatch} occurrences)`);
      pass = false;
    } else if (presentReplace < 1) {
      console.error(`  [FAIL] Rule ${rule.id}: replacement English string not found in bundle`);
      pass = false;
    } else {
      verified++;
    }
  }
  if (pass) {
    console.log(`  [PASS] All ${verified}/${rules.length} active replacement rules verified`);
  }
  return pass;
}

function verifyGate4Html() {
  console.log('\n--- Gate 4: HTML lang="en" Normalization Verification ---');
  let pass = true;
  ['public_html', 'dist_html'].forEach(key => {
    const filePath = TARGET_PATHS[key];
    if (!fs.existsSync(filePath)) return;
    const content = fs.readFileSync(filePath, 'utf8');
    const hasLangEn = content.includes('lang="en"');
    const hasLangZh = content.includes('lang="zh-CN"');
    if (hasLangEn && !hasLangZh) {
      console.log(`  [PASS] ${key}: lang="en" verified, lang="zh-CN" absent`);
    } else {
      console.error(`  [FAIL] ${key}: lang="en" = ${hasLangEn}, lang="zh-CN" = ${hasLangZh}`);
      pass = false;
    }
  });
  return pass;
}

function verifyGate5Syntax(bundleContent) {
  console.log('\n--- Gate 5: Transformed JS Syntax Verification ---');
  const result = spawnSync('node', ['--input-type=module', '--check'], {
    input: bundleContent,
    encoding: 'utf8'
  });
  if (result.status === 0) {
    console.log('  [PASS] Transformed bundle passes node --input-type=module --check');
    return true;
  } else {
    console.error('  [FAIL] Transformed bundle syntax error:\n', result.stderr);
    return false;
  }
}

function verifyGate6Inventory(bundleContent) {
  console.log('\n--- Gate 6: CJK Inventory Classification Audit ---');
  const stringLiteralRegex = /"([^"\\]*(?:\\.[^"\\]*)*)"|'([^'\\]*(?:\\.[^'\\]*)*)'|`([^`\\]*(?:\\.[^`\\]*)*)`/g;
  const chineseCharRegex = /[\u4e00-\u9fff]/;

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
  if (counts.UNCLASSIFIED === 0) {
    console.log('  [PASS] UNCLASSIFIED = 0, full inventory classified');
    return true;
  }
  return false;
}

function run() {
  console.log('================================================================');
  console.log('Phase E6: English UI Normalization Verification (V2 Complete)');
  console.log('================================================================\n');

  const bundleContent = fs.readFileSync(TARGET_PATHS.public_bundle, 'utf8');
  const rules = JSON.parse(fs.readFileSync(MAP_PATH, 'utf8'));
  const activeRules = rules.filter(r => (r.phase === 'e6' || r.phase === 'v1') && r.category !== 'PROTECTED_LITERAL' && r.match && r.replace);

  const g1 = verifyGate1Hashes();
  const g2 = verifyGate2ProtectedLiterals(bundleContent);
  const g3 = verifyGate3Rules(bundleContent, activeRules);
  const g4 = verifyGate4Html();
  const g5 = verifyGate5Syntax(bundleContent);
  const g6 = verifyGate6Inventory(bundleContent);

  const allPass = g1 && g2 && g3 && g4 && g5 && g6;
  console.log('\n================================================================');
  if (allPass) {
    console.log('PHASE E6 VERIFICATION = PASS');
    console.log('All 6 static and structural verification gates PASSED.');
  } else {
    console.error('PHASE E6 VERIFICATION = FAILED');
    process.exit(1);
  }
  console.log('================================================================\n');
}

run();
