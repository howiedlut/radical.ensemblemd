__author__    = "Vivek Balasubramanian <vivek.balasubramanian@rutgers.edu>"
__copyright__ = "Copyright 2016, http://radical.rutgers.edu"
__license__   = "MIT"

from radical.entk import EoP, AppManager, Kernel, ResourceHandle

from meshfem import meshfem_kernel
from specfem import specfem_kernel
ENSEMBLE_SIZE=1


class Test(EoP):

    def __init__(self, ensemble_size, pipeline_size):
        super(Test,self).__init__(ensemble_size, pipeline_size)

    def stage_1(self, instance):
        global ENSEMBLE_SIZE

        k1 = Kernel(name="meshfem")
        k1.arguments = []
        k1.copy_input_data = [  '$SHARED/ipdata.tar']
        k1.cores = 4
        k1.mpi=True

        return k1

   

if __name__ == '__main__':

    # Create an application manager
    app = AppManager(name='seisflow')

    # Register kernels to be used
    app.register_kernels(meshfem_kernel)
    app.register_kernels(specfem_kernel)

    # Create a resource handle for target machine
    res = ResourceHandle(resource="local.localhost",
                cores=4,
                #username='vivek91',
                #project = 'TG-MCB090174',
                #queue='development',
                walltime=10,
                database_url='mongodb://rp:rp@ds015335.mlab.com:15335/rp')

    res.shared_data = [ './input_data/ipdata.tar']

    try:

        # Submit request for resources + wait till job becomes Active
        res.allocate(wait=True)

        # Create pattern object with desired ensemble size, pipeline size
        pipe = Test(ensemble_size=ENSEMBLE_SIZE, pipeline_size=1)

        # Add workload to the application manager
        app.add_workload(pipe)

        # Run the given workload
        res.run(app)

    except Exception, ex:
        print 'Application failed, error: ', ex


    finally:
        # Deallocate the resource
        res.deallocate()
    