from pathlib import Path

import argparse
from containers.config import Config
from containers.constants import *
from experiment import MainExperiment
from containers.task_context import ContinuousSelector, NetGenTaskContext, PathTaskContext

if __name__ == '__main__':
    # set the number of workers here
    parser = argparse.ArgumentParser(description='Model arguments')
    parser.add_argument('--dir', default='wd/new_exp', type=str, help='Result directory')
    parser.add_argument('--kwargs', default='{}', help='args to be added to the config')
    parser.add_argument('--task_context_kwargs', default='{}', help='args to be added to the task_context')
    args = parser.parse_args()

    task = PathTaskContext(**{
        'single_approach':True,
        'dir':Path(args.dir),
        'penetration_rate':0.0,
        'aadt_conversion_factor':0.055,
        **eval(args.task_context_kwargs)
    })
    peak_or_off_peak = 'peak' if task.aadt_conversion_factor == 0.084 * throughput_threshold else 'off-peak'

    # Use this configuration if you want to define intersections programatically.
    # task = NetGenTaskContext(
    #     base_id=[42],
    #     penetration_rate=[0.1],
    #     single_approach=True,
    #     inflow=ContinuousSelector(200, 400, 4),
    #     lane_length=ContinuousSelector(50, 750, 4),
    #     speed_limit=ContinuousSelector(6.5, 30, 4),
    #     green_phase=ContinuousSelector(15, 35, 3), 
    #     red_phase=ContinuousSelector(30, 55, 4),  
    #     offset=ContinuousSelector(0, 1, 5),
    #     # inflow=ContinuousSelector(200, 400, 3),
    #     # lane_length=ContinuousSelector(75, 600,4),
    #     # speed_limit=ContinuousSelector(10, 20, 3), 
    #     # green_phase=ContinuousSelector(25, 35, 3),
    #     # red_phase=ContinuousSelector(30, 45, 3),
    #     # offset=0,       
    # )

    # training config
    config = Config(
        run_mode='train',
        task_context=task,
        working_dir=Path(args.dir),

        wandb_proj='greenwave_final_models',
        visualize_sumo=False,
        
        stop_penalty=35,
        emission_penalty=3,
        fleet_reward_ratio=0.0,
        
        moves_emissions_models=['68_46'], 
    )

    # moves_emissions_models_config=['54_72',]
    # moves_emissions_models_conditions_config=[REGULAR for _ in range(len(moves_emissions_models_config))]
    
    # evaluation config
    # config = Config(
    #     trajectories_output=False,
    #     run_mode='full_eval',
    #     task_context=task,
    #     working_dir=Path(args.dir),

    #     enable_wandb=False,
    #     visualize_sumo=False,
        
    #     stop_penalty=35,
    #     emission_penalty=3,
    #     fleet_reward_ratio=0.0,
        
    #     episode_to_eval=5000,
        
    #     moves_emissions_models=moves_emissions_models_config,
    #     moves_emissions_models_conditions=moves_emissions_models_conditions_config,
        
    #     full_eval_run_baselines=False,
    #     n_steps=3,
    #     report_uncontrolled_region_metrics=True,
    #     csv_output_custom_name=(str(task.dir)).split('/')[-1] + '_' + peak_or_off_peak + '_' + str(throughput_threshold),
    # )

    # sumo visualization config
    # config = Config(
    #     run_mode='single_eval',
    #     task_context=task,
    #     working_dir=Path(args.dir),

    #     stop_penalty=35,
    #     emission_penalty=3, 
    #     fleet_reward_ratio=0.0,

    #     enable_wandb=False,
    #     visualize_sumo=True,

    #     episode_to_eval=700,
    #     parallelization_size=1,
    #     moves_emissions_models=['44_64'],
    # )
    assert len(config.moves_emissions_models) == len(config.moves_emissions_models_conditions), "The evaluations conditions do not have the same dimensions"
    config = config.update({**eval(args.kwargs)})

    main_exp = MainExperiment(config)

    # run experiment
    main_exp.run()
