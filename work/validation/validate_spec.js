const fs = require('fs');
const yaml = require('yaml');

// Read the spec file
const specPath = process.argv[2];
const specContent = fs.readFileSync(specPath, 'utf8');

// Parse YAML
let spec;
try {
  spec = yaml.parse(specContent);
  console.log('✓ YAML syntax is valid');
} catch (e) {
  console.error('✗ YAML syntax error:', e.message);
  process.exit(1);
}

// Validation results
const results = {
  spec_file: specPath,
  timestamp: new Date().toISOString(),
  validation_status: 'PASS',
  approval: 'APPROVED',
  summary: '',
  critical_issues: [],
  warnings: [],
  recommendations: []
};

// Required fields from CONTRACT.md
const requiredFields = {
  version: 'string',
  units: 'string',
  assumptions: 'array',
  overall: 'object',
  walls: 'object',
  roof: 'object',
  openings: 'object',
  materials: 'object',
  tolerances: 'object',
  coordinate_system: 'object'
};

// Check required top-level fields
console.log('\n=== REQUIRED FIELD VALIDATION ===');
for (const [field, expectedType] of Object.entries(requiredFields)) {
  if (!(field in spec)) {
    results.critical_issues.push(`Missing required field: ${field}`);
    console.log(`✗ Missing: ${field}`);
  } else {
    const actualType = Array.isArray(spec[field]) ? 'array' : typeof spec[field];
    if (actualType !== expectedType) {
      results.critical_issues.push(`Field '${field}' has wrong type: expected ${expectedType}, got ${actualType}`);
      console.log(`✗ Wrong type: ${field} (expected ${expectedType}, got ${actualType})`);
    } else {
      console.log(`✓ ${field}: ${expectedType}`);
    }
  }
}

// Check version format (v###)
console.log('\n=== VERSION FORMAT VALIDATION ===');
if (spec.version && !/^v\d{3}$/.test(spec.version)) {
  results.warnings.push(`Version format '${spec.version}' should be v### (3 digits)`);
  console.log(`⚠ Version format should be v### (3 digits), got: ${spec.version}`);
} else {
  console.log(`✓ Version format: ${spec.version}`);
}

// Check overall structure
console.log('\n=== OVERALL STRUCTURE VALIDATION ===');
const overallRequired = ['footprint', 'height'];
if (spec.overall) {
  for (const field of overallRequired) {
    if (!(field in spec.overall)) {
      results.critical_issues.push(`Missing overall.${field}`);
      console.log(`✗ Missing: overall.${field}`);
    } else {
      console.log(`✓ overall.${field}`);
    }
  }

  // Check height fields
  if (spec.overall.height) {
    const heightFields = ['wall_height', 'parapet_height', 'total_height'];
    for (const field of heightFields) {
      if (!(field in spec.overall.height)) {
        results.critical_issues.push(`Missing overall.height.${field}`);
        console.log(`✗ Missing: overall.height.${field}`);
      } else if (typeof spec.overall.height[field] !== 'number') {
        results.critical_issues.push(`overall.height.${field} must be a number`);
        console.log(`✗ Wrong type: overall.height.${field}`);
      } else {
        console.log(`✓ overall.height.${field}: ${spec.overall.height[field]}`);
      }
    }
  }
}

// Check walls structure
console.log('\n=== WALLS STRUCTURE VALIDATION ===');
const wallsRequired = ['thickness', 'material', 'height'];
if (spec.walls) {
  for (const field of wallsRequired) {
    if (!(field in spec.walls)) {
      results.critical_issues.push(`Missing walls.${field}`);
      console.log(`✗ Missing: walls.${field}`);
    } else {
      console.log(`✓ walls.${field}`);
    }
  }
}

// Check roof structure
console.log('\n=== ROOF STRUCTURE VALIDATION ===');
const roofRequired = ['type', 'thickness', 'elevation'];
if (spec.roof) {
  for (const field of roofRequired) {
    if (!(field in spec.roof)) {
      results.critical_issues.push(`Missing roof.${field}`);
      console.log(`✗ Missing: roof.${field}`);
    } else {
      console.log(`✓ roof.${field}`);
    }
  }
}

// Check openings structure
console.log('\n=== OPENINGS STRUCTURE VALIDATION ===');
if (spec.openings) {
  if (!('doors' in spec.openings) && !('windows' in spec.openings)) {
    results.warnings.push('openings section has no doors or windows');
    console.log('⚠ No doors or windows defined');
  } else {
    console.log(`✓ openings.doors: ${spec.openings.doors?.length || 0} doors`);
    console.log(`✓ openings.windows: ${spec.openings.windows?.length || 0} windows`);
  }

  // Validate door fields
  if (spec.openings.doors) {
    spec.openings.doors.forEach((door, i) => {
      const doorRequired = ['id', 'type', 'width', 'height', 'wall', 'position'];
      doorRequired.forEach(field => {
        if (!(field in door)) {
          results.critical_issues.push(`Door ${i} missing field: ${field}`);
          console.log(`✗ Door ${i} missing: ${field}`);
        }
      });

      // Validate wall reference
      if (door.wall && !['front', 'left', 'right', 'rear'].includes(door.wall)) {
        results.critical_issues.push(`Door ${door.id} has invalid wall reference: ${door.wall}`);
        console.log(`✗ Door ${door.id} invalid wall: ${door.wall}`);
      }
    });
  }

  // Validate window fields
  if (spec.openings.windows) {
    spec.openings.windows.forEach((window, i) => {
      const windowRequired = ['id', 'width', 'height', 'wall', 'position'];
      windowRequired.forEach(field => {
        if (!(field in window)) {
          results.critical_issues.push(`Window ${i} missing field: ${field}`);
          console.log(`✗ Window ${i} missing: ${field}`);
        }
      });

      // Validate wall reference
      if (window.wall && !['front', 'left', 'right', 'rear'].includes(window.wall)) {
        results.critical_issues.push(`Window ${window.id} has invalid wall reference: ${window.wall}`);
        console.log(`✗ Window ${window.id} invalid wall: ${window.wall}`);
      }
    });
  }
}

// Check materials structure
console.log('\n=== MATERIALS STRUCTURE VALIDATION ===');
const materialsRequired = ['walls', 'roof', 'door', 'windows'];
if (spec.materials) {
  for (const field of materialsRequired) {
    if (!(field in spec.materials)) {
      results.critical_issues.push(`Missing materials.${field}`);
      console.log(`✗ Missing: materials.${field}`);
    } else if (typeof spec.materials[field] !== 'string') {
      results.critical_issues.push(`materials.${field} must be a string`);
      console.log(`✗ Wrong type: materials.${field}`);
    } else {
      console.log(`✓ materials.${field}: ${spec.materials[field]}`);
    }
  }
}

// Check tolerances structure
console.log('\n=== TOLERANCES STRUCTURE VALIDATION ===');
const tolerancesRequired = ['dimension_tolerance', 'angle_tolerance_degrees', 'allow_non_manifold'];
if (spec.tolerances) {
  for (const field of tolerancesRequired) {
    if (!(field in spec.tolerances)) {
      results.critical_issues.push(`Missing tolerances.${field}`);
      console.log(`✗ Missing: tolerances.${field}`);
    } else {
      console.log(`✓ tolerances.${field}`);
    }
  }
}

// Check coordinate_system structure
console.log('\n=== COORDINATE SYSTEM VALIDATION ===');
const coordRequired = ['origin', 'axes'];
if (spec.coordinate_system) {
  for (const field of coordRequired) {
    if (!(field in spec.coordinate_system)) {
      results.critical_issues.push(`Missing coordinate_system.${field}`);
      console.log(`✗ Missing: coordinate_system.${field}`);
    } else {
      console.log(`✓ coordinate_system.${field}`);
    }
  }

  if (spec.coordinate_system.axes) {
    ['x', 'y', 'z'].forEach(axis => {
      if (!(axis in spec.coordinate_system.axes)) {
        results.critical_issues.push(`Missing coordinate_system.axes.${axis}`);
        console.log(`✗ Missing: coordinate_system.axes.${axis}`);
      } else {
        console.log(`✓ coordinate_system.axes.${axis}: ${spec.coordinate_system.axes[axis]}`);
      }
    });
  }
}

// Check internal consistency
console.log('\n=== INTERNAL CONSISTENCY VALIDATION ===');
if (spec.overall?.height) {
  const wh = spec.overall.height.wall_height;
  const ph = spec.overall.height.parapet_height;
  const th = spec.overall.height.total_height;

  if (wh !== undefined && ph !== undefined && th !== undefined) {
    const calculated = wh + ph;
    const diff = Math.abs(calculated - th);
    if (diff > 0.01) {
      results.warnings.push(`total_height (${th}) should equal wall_height (${wh}) + parapet_height (${ph}) = ${calculated}`);
      console.log(`⚠ Height mismatch: ${wh} + ${ph} = ${calculated}, but total_height = ${th}`);
    } else {
      console.log(`✓ total_height = wall_height + parapet_height`);
    }
  }
}

if (spec.walls?.height !== undefined && spec.roof?.elevation !== undefined) {
  if (spec.walls.height !== spec.roof.elevation) {
    results.warnings.push(`roof.elevation (${spec.roof.elevation}) should match walls.height (${spec.walls.height})`);
    console.log(`⚠ roof.elevation (${spec.roof.elevation}) ≠ walls.height (${spec.walls.height})`);
  } else {
    console.log(`✓ roof.elevation matches walls.height`);
  }
}

// Check for positive dimensions
console.log('\n=== DIMENSION VALIDATION ===');
const checkPositive = (obj, path = '') => {
  for (const [key, value] of Object.entries(obj)) {
    const fullPath = path ? `${path}.${key}` : key;
    if (typeof value === 'number') {
      if (key.includes('height') || key.includes('width') || key.includes('depth') ||
          key.includes('thickness') || key.includes('diameter') || key.includes('elevation')) {
        if (value < 0) {
          results.critical_issues.push(`${fullPath} must be positive, got ${value}`);
          console.log(`✗ Negative dimension: ${fullPath} = ${value}`);
        } else if (value === 0 && !key.includes('sill_height') && !key.includes('position')) {
          results.warnings.push(`${fullPath} is zero, which may be unintentional`);
          console.log(`⚠ Zero dimension: ${fullPath}`);
        } else {
          console.log(`✓ ${fullPath}: ${value}`);
        }
      }
    } else if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      checkPositive(value, fullPath);
    }
  }
};

checkPositive(spec);

// Traceability check
console.log('\n=== TRACEABILITY VALIDATION ===');
if (spec.assumptions && Array.isArray(spec.assumptions)) {
  const hasAnalysisRef = spec.assumptions.some(a =>
    typeof a === 'string' && (a.includes('analysis') || a.includes('reference'))
  );
  if (!hasAnalysisRef) {
    results.recommendations.push('Consider adding reference to source analysis in assumptions');
    console.log('⚠ No explicit reference to analysis document in assumptions');
  } else {
    console.log('✓ Assumptions reference analysis');
  }
} else {
  console.log('⚠ No assumptions list found');
}

// Final status determination
console.log('\n=== VALIDATION SUMMARY ===');
if (results.critical_issues.length > 0) {
  results.validation_status = 'FAIL';
  results.approval = 'REJECTED';
  results.summary = `Validation failed with ${results.critical_issues.length} critical issue(s)`;
  console.log(`✗ FAIL: ${results.critical_issues.length} critical issue(s)`);
} else if (results.warnings.length > 0) {
  results.validation_status = 'PASS_WITH_WARNINGS';
  results.approval = 'APPROVED_WITH_CONDITIONS';
  results.summary = `Validation passed with ${results.warnings.length} warning(s)`;
  console.log(`⚠ PASS WITH WARNINGS: ${results.warnings.length} warning(s)`);
} else {
  results.validation_status = 'PASS';
  results.approval = 'APPROVED';
  results.summary = 'All validation checks passed';
  console.log('✓ PASS: All checks passed');
}

console.log(`\nWarnings: ${results.warnings.length}`);
console.log(`Recommendations: ${results.recommendations.length}`);

// Write results
const outputPath = specPath.replace(/building_v\d+\.yaml$/, 'spec_v002_validation.json').replace(/spec/, 'validation');
fs.mkdirSync(require('path').dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
console.log(`\n✓ Validation report written to: ${outputPath}`);
