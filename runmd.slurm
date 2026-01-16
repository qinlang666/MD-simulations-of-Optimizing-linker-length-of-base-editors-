#!/bin/sh
#SBATCH --job-name=gromacs
#SBATCH --partition=56c1t8n
#SBATCH --nodes=1                              
#SBATCH --ntasks-per-node=8            
#SBATCH--gres=gpu:1
#SBATCH--mem-per-cpu=15000MB
#SBATCH--account=linqiupeng_lab
#SBATCH --error=%j.err
#SBATCH --output=%j.out
CURDIR=`pwd`
rm -rf $CURDIR/nodelist.$SLURM_JOB_ID
NODES=`scontrol show hostnames $SLURM_JOB_NODELIST`
for i in $NODES
do
echo "$i:$SLURM_NTASKS_PER_NODE" >> $CURDIR/nodelist.$SLURM_JOB_ID
done
echo "process will start at : "
 date
 echo "++++++++++++++++++++++++++++++++++++++++"
module load gromacs/2024.4
gmx mdrun -v -deffnm md
 echo "++++++++++++++++++++++++++++++++++++++++"
 echo "process end at : "
 date
