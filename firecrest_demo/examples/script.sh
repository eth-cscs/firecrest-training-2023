#!/bin/bash -l

#SBATCH --job-name=firecrest_job_test
#SBATCH --time=10:00
#SBATCH --nodes=2
#SBATCH --reservation=firecrest_api
#SBATCH -Cgpu
#SBATCH -Aclass08

# Very silly script
srun hostname
sleep 100
srun echo 'Bye'
