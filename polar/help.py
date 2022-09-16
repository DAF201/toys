helper = """
log: display the tree
log <target_dir>

add: add files to an dir, will not replace is file already exist
    add <target_dir> <target_files1> <target_files2>...

delete: delete files from an dir
delete <target_dir> <target_file1> <target_file2>...

fetch: fetch files from an dir
fetch <target_dir> <target_file1> <target_file2>...

archive: make an archive of files in current folder, will replace files if exist
archive <target_dir>

destroy: destroy all the files in an dir
destroy <target_dir>

restore: restore files in current folder to an archive, every file not included will be removed
restore <target_dir>
"""
