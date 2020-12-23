% The simulator to run a workspace simulation for rays
%
% Author        : Jonathan EDEN
% Created       : 2017
% Description    :
%   Workspace simulator generates the workspace over a defined set of space
%   (currently only a grid of states is accepted). The workspace is created
%   using the ray method
classdef RayWorkspaceSimulator < SimulatorBase
    
    properties
        grid                    % Grid object for brute force workspace (input)
        workspace               % Final Workspace (output)
    end
    
    properties (SetAccess = private)
        comp_time_total             % Total time to compute workspace
        comp_time_evaluation        % Time to just evaluate the workspace points
        comp_time_graph             % Time to construct the graph structure
        
        free_variable_length    % The number of rays for each free variable
        conditions = []         % A list of conditions to be evaluated for
        metrics = []            % A list of metrics to be evaluated for
    end
    properties (Hidden)
        
    end
    
    methods
        % The constructor for the workspace simulator class.
        function w = RayWorkspaceSimulator(model,grid,conditions,metrics)
            w@SimulatorBase(model);
            w.grid          = grid;
            w.conditions    = conditions;
            w.metrics       = metrics;
        end
        
        % Implementation of the run function
        function run(obj)
            
            % Test if the metrics have infinite limits
            for i = 1:size(obj.metrics,2)
                if((~isempty(obj.metrics{i}.metricMax))&&((abs(obj.metrics{i}.metricMax)==Inf)||(abs(obj.metrics{i}.metricMin)==Inf)))
                    CASPR_log.Print('A metric with infinite limit values cannot be plotted.  To plot please set the metric limit to be finite or filter the workspace after plotting',CASPRLogLevel.WARNING);
                end
            end
            
            
            n_grid_points = 0;
            for i =1:size(obj.grid.dim_disc_ia)
                grid_index = true(obj.grid.n_dimensions,1); grid_index(i) = false;
                obj.free_variable_length(i) = prod(obj.grid.q_length(grid_index));
                n_grid_points = n_grid_points + obj.free_variable_length(i);
            end
            
            workspace_count = 0;
            obj.workspace = RayWorkspace(obj.model, obj.grid);

            % Runs over each dimension and construct the rays for that
            % dimension
            % each point
            k = 1;
            ray_t_in = tic;
            total_t_in = tic;
            for i = 1:obj.grid.n_dimensions

                if ismember(i,obj.grid.dim_disc_ia) 
                %i is the free variable index;
                grid_index = true(obj.grid.n_dimensions,1); grid_index(i) = false;
                % Create a subgrid
                sub_grid = UniformGrid(obj.grid.q_begin(grid_index),obj.grid.q_end(grid_index),obj.grid.delta_q(grid_index),'step_size',obj.grid.q_wrap(grid_index));
                for j = 1:sub_grid.n_points
                CASPR_log.Print([sprintf('Workspace DoF %d. ',i),sprintf('Workspace ray %d. ',j),sprintf('Completion Percentage: %3.2f',100*k/n_grid_points)],CASPRLogLevel.INFO);  
                    % Load the current fixed grid coordinates
                    q_fixed = sub_grid.getGridPoint(j);
                    % Construct the workspace ray
                    wr = RayWorkspaceElement(obj.model,q_fixed,obj.metrics,obj.conditions,...
                        i,[obj.grid.q_begin(i),obj.grid.q_end(i)]);
                    
                    % Determine whether to add the condition to the workspace
                    test_conditions = cellfun(@isempty,wr.conditions);
                    % Determine whether to add to workspace
                    if ~all(test_conditions)
                        entry_condition = 1;
                    else
                        entry_condition = 0;
                    end                    
                    if(entry_condition)
                        % Add the workspace ray to the
                        obj.workspace.rays{k} = wr;
                        workspace_count = workspace_count + 1;
                    end
                    k = k+1;
                end
                end
             end 
%             obj.workspace.rays = obj.workspace.rays(~cellfun('isempty',obj.workspace.rays));            
            obj.comp_time_evaluation = toc(ray_t_in);
            graph_t_in = tic;
            obj.comp_time_graph = toc(graph_t_in);
            obj.comp_time_total = toc(total_t_in);
        end
    end
end
