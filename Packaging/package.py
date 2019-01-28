#!/usr/bin/env python3
from ue4helpers import ArchiveUtils, FilesystemUtils, PlatformInfo, PluginPackager, VersionHelpers
from os.path import abspath, dirname, join
import shutil, sys


# The location of the Substance plugin source code
SUBSTANCE_ZIP_URL = 'https://s3-us-west-1.amazonaws.com/deepdrive/substance/SubstanceUE4_Plugin_Public_4.21.0.31.zip'


# Verify that we are running under Linux, since Allegorithmic already provides Windows and Mac binaries
if PlatformInfo.identifier() != 'Linux':
	print('Not running under Linux, nothing to do.')
	sys.exit(0)

# Remove any existing source code for the Substance plugin
repoRoot = dirname(dirname(abspath(__file__)))
sourceRoot = join(repoRoot, 'Substance')
FilesystemUtils.remove(sourceRoot)

# Download and extract the latest source code for the Substance plugin
print('Downloading and extracting the source code for the Substance plugin...')
ArchiveUtils.extract(SUBSTANCE_ZIP_URL, sourceRoot)

# Create our plugin packager
packager = PluginPackager(
	sourceRoot,
	version = VersionHelpers.from_descriptor(),
	archive = '{name}-{version}-Desktop',
	stage = [
		'DLLs',
		'Include',
		'Libs',
		join('Intermediate', 'Build', 'Win32'),
		join('Intermediate', 'Build', 'Win64'),
		join('Intermediate', 'Build', 'Mac'),
		join('Binaries', 'Win64'),
		join('Binaries', 'Mac')
	]
)

# Clean any previous Linux build artifacts (leaving Windows and Mac binaries intact)
packager.clean(preserve=True)

# Package the plugin, merging the Windows and Mac binaries into the packaged distribution
packager.package()

# Compress the packaged distribution
archive = packager.archive()

# TODO: upload the archive to Amazon S3
print('Created compressed archive "{}".'.format(archive))
