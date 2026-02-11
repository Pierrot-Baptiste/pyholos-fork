import subprocess
from pathlib import Path, PureWindowsPath
from typing import Optional, Iterator

from pyholos.config import PATH_HOLOS_CLI
from pyholos.utils import print_holos_msg


def set_cmd(
        path_dir_farms: Path,
        path_dir_outputs: Optional[Path] = None,
        name_farm_json: Optional[str] = None,
        name_dir_farms_json: Optional[str] = None,
        name_settings: Optional[str] = None,
        id_slc_polygon: Optional[int] = None,
) -> list[str]:
    cmd = [
        # 'cmd',
        # '/c',
        str(PureWindowsPath(PATH_HOLOS_CLI)),
        str(PureWindowsPath(path_dir_farms)),
        '-u',
        'metric'
    ]

    if path_dir_outputs is not None:
        cmd += [
            '-o',
            str(PureWindowsPath(path_dir_outputs))
        ]

    if name_farm_json is not None:
        cmd += [
            '-i',
            name_farm_json
        ]

    if name_dir_farms_json is not None:
        cmd += [
            '-f',
            name_dir_farms_json
        ]

    if name_settings is not None:
        if any([name_farm_json is not None, name_dir_farms_json is not None]):
            cmd += [
                '-s',
                name_settings
            ]

    if id_slc_polygon is not None:
        cmd += [
            '-p',
            str(int(id_slc_polygon))
        ]

    return cmd


def launch_holos(
        path_dir_farms: Path,
        path_dir_outputs: Optional[Path] = None,
        name_farm_json: Optional[str] = None,
        name_dir_farms_json: Optional[str] = None,
        name_settings: Optional[str] = None,
        id_slc_polygon: Optional[int] = None,
        is_print_holos_messages: bool = False
) -> None:
    cmd = set_cmd(
        path_dir_farms=path_dir_farms,
        path_dir_outputs=path_dir_outputs,
        name_farm_json=name_farm_json,
        name_dir_farms_json=name_dir_farms_json,
        name_settings=name_settings,
        id_slc_polygon=id_slc_polygon
    )

    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(PureWindowsPath(path_dir_farms)),
        shell=False
    )

    assert process.stdin is not None
    assert process.stdout is not None
    assert process.stderr is not None

    for msg in _get_cli_messages(p=process):
        print_holos_msg(
            is_print_message=is_print_holos_messages,
            holos_message=msg
        )

        if "import from the holos gui" in msg.lower():
            process.stdin.write('no\n')
            process.stdin.flush()
        elif "press enter to exit" in msg.lower():
            process.stdin.write('\n')
            process.stdin.flush()
        elif "run another scenario" in msg.lower():  # New prompt from cli?
            process.stdin.write('N\n')
            process.stdin.flush()

    # # for debugging
    # rc = process.wait(timeout=60)
    # err = process.stderr.read() if process.stderr else ""
    # print_holos_msg(True, f"[RETURNCODE] {rc}")
    # if err:
    #     print_holos_msg(True, f"[STDERR] {err}")


def _get_cli_messages(p: subprocess.Popen) -> Iterator[str]:
    assert p.stdout is not None
    while True:
        line = p.stdout.readline()
        if not line:
            # If process ended or no more output, stop
            if p.poll() is not None:
                break
            continue
        # returns None while subprocess is running
        yield line
