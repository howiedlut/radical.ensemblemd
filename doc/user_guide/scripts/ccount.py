import sys
import os
import json

from radical.ensemblemd import Kernel
from radical.ensemblemd import BagofTasks
from radical.ensemblemd import EnsemblemdError
from radical.ensemblemd import SingleClusterEnvironment


# ------------------------------------------------------------------------------
#
class CharCount(BagofTasks):
	"""The CharCount class implements a three-stage BagofTasks. It inherits from
		radical.ensemblemd.BagofTasks, the abstract base class for all BagofTaskss.
	"""

	def __init__(self, stages, instances):
		BagofTasks.__init__(self, stages, instances)

	def stage_1(self, instance):
		"""The first stage of the BagofTasks creates a 1 MB ASCI file.
		"""
		k = Kernel(name="misc.mkfile")
		k.arguments = ["--size=1000000", "--filename=asciifile-{0}.dat".format(instance)]
		return k

	def stage_2(self, instance):
		"""The second stage of the BagofTasks does a character frequency analysis
		   on the file generated the first stage. 
		"""

		k = Kernel(name="misc.ccount")
		k.arguments            = ["--inputfile=asciifile-{0}.dat".format(instance), "--outputfile=cfreqs-{0}.dat".format(instance)]
		k.link_input_data      = "$STAGE_1/asciifile-{0}.dat".format(instance)
		return k

	def stage_3(self, instance):
		"""The third stage of the BagofTasks creates a checksum of the output file
		   of the second stage. The result is transferred back to the host
		   running this script.
		"""
		k = Kernel(name="misc.chksum")
		k.arguments            = ["--inputfile=cfreqs-{0}.dat".format(instance), "--outputfile=cfreqs-{0}.sha1".format(instance)]
		k.link_input_data      = "$STAGE_2/cfreqs-{0}.dat".format(instance)
		k.download_output_data = "cfreqs-{0}.sha1".format(instance)
		return k

# ------------------------------------------------------------------------------
#
if __name__ == "__main__":


	try:

		# Create a new resource handle with one resource and a fixed
		# number of cores and runtime.
		cluster = SingleClusterEnvironment(
			resource="localhost",
			cores=1,
			walltime=15,
			username=None,
			project=None,
			database_url='mongodb://entk_user:entk_user@ds029224.mlab.com:29224/entk_doc',
			)

		# Allocate the resources. 
		cluster.allocate()

		# Set the 'instances' of the BagofTasks to 16. This means that 16 instances
		# of each BagofTasks stage are executed.
		#
		# Execution of the 16 BagofTasks instances can happen concurrently or
		# sequentially, depending on the resources (cores) available in the
		# SingleClusterEnvironment.
		ccount = CharCount(stages=3,instances=16)

		cluster.run(ccount)


		# Deallocate the resources. 
		cluster.deallocate()

		# Print the checksums
		print "\nResulting checksums:"
		import glob
		for result in glob.glob("cfreqs-*.sha1"):
			print "  * {0}".format(open(result, "r").readline().strip())

	except EnsemblemdError, er:

		print "Ensemble MD Toolkit Error: {0}".format(str(er))
		raise # Just raise the execption again to get the backtrace