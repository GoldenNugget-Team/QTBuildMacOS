"""Verify every Mach-O payload in the shared Universal2 Qt wheels."""
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile
from packaging.utils import parse_wheel_filename
wheel_paths = list(Path(sys.argv[1]).glob('*.whl'))
names = {parse_wheel_filename(p.name)[0] for p in wheel_paths}
assert names == {'pyside6', 'shiboken6'}, names
magics = {b'\xfe\xed\xfa\xce', b'\xce\xfa\xed\xfe', b'\xfe\xed\xfa\xcf',
          b'\xcf\xfa\xed\xfe', b'\xca\xfe\xba\xbe', b'\xbe\xba\xfe\xca',
          b'\xca\xfe\xba\xbf', b'\xbf\xba\xfe\xca'}
for wheel_path in wheel_paths:
    tags = parse_wheel_filename(wheel_path.name)[3]
    assert all(tag.platform.endswith('_universal2') for tag in tags), wheel_path
    binaries = 0
    with zipfile.ZipFile(wheel_path) as wheel, tempfile.TemporaryDirectory() as tmp:
        binary = Path(tmp) / 'binary'
        for entry in wheel.infolist():
            with wheel.open(entry) as stream:
                if stream.read(4) not in magics:
                    continue
            binary.write_bytes(wheel.read(entry))
            slices = set(subprocess.check_output(['lipo', '-archs', str(binary)], text=True).split())
            assert {'arm64', 'x86_64'} <= slices, (wheel_path, entry.filename, slices)
            binaries += 1
    assert binaries, f'No Mach-O binaries found in {wheel_path}'
    print(f'Universal2 wheel verified: {wheel_path.name} ({binaries} binaries)')
