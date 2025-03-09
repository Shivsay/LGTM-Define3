import React, { useEffect, useRef, useState } from "react";
import "dhtmlx-gantt/codebase/dhtmlxgantt.css";
import { gantt } from "dhtmlx-gantt";

const FlightGanttChart = () => {
  const ganttContainer = useRef(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    // Configure gantt
    gantt.config.date_format = "%Y-%m-%d %H:%i";
    gantt.config.scale_unit = "day";
    gantt.config.date_scale = "%d %M";
    gantt.config.subscales = [
      { unit: "hour", step: 1, date: "%H:%i" }
    ];
    
    // Configure columns
    gantt.config.columns = [
      { name: "text", label: "Activity", tree: true, width: 200 },
      { name: "aircraft", label: "Aircraft", align: "center", width: 80 },
      { name: "type", label: "Type", align: "center", width: 80 },
      { name: "stations", label: "Route", align: "center", width: 100 },
      { name: "start_date", label: "Start Time", align: "center", width: 140 },
      { name: "end_date", label: "End Time", align: "center", width: 140 }
    ];
    
    // Custom task appearance based on type
    gantt.templates.task_class = function(start, end, task) {
      if (task.type === "preassignment") {
        return "preassignment-task";
      } else if (task.type === "flight") {
        return "flight-task";
      }
      return "";
    };
    
    // Add custom CSS for task appearance
    const style = document.createElement("style");
    style.innerHTML = `
      .preassignment-task .gantt_task_progress,
      .preassignment-task .gantt_task_content {
        background-color: #FFA500;
        color: white;
      }
      
      .flight-task .gantt_task_progress,
      .flight-task .gantt_task_content {
        background-color: #4B8CDC;
        color: white;
      }
      
      .gantt_task_line.gantt_task_parent {
        background-color: #eee;
        height: 30px;
      }
      
      .gantt_task_content {
        font-weight: bold;
      }
    `;
    document.head.appendChild(style);
    
    // Initialize gantt
    gantt.init(ganttContainer.current);
    
    // Fetch data from API
    const fetchTailAssignments = async () => {
      setLoading(true);
      try {
        const response = await fetch("http://127.0.0.1:8000/api?maintain_trips=False");
        
        if (!response.ok) {
          throw new Error(`Failed to fetch data: ${response.status}`);
        }
        
        const tailAssignments = await response.json();
        
        // Transform data for gantt
        const tasks = {
          data: [],
          links: []
        };
        
        let taskId = 1;
        
        // Create parent tasks for each aircraft
        tailAssignments.assignments.forEach((assignment, index) => {
          const parentId = taskId++;
          
          // Add aircraft as parent task
          tasks.data.push({
            id: parentId,
            text: assignment.aircraft,
            aircraft: assignment.aircraft,
            type: "aircraft",
            open: true,
            render: "split" // Shows all subtasks
          });
          
          // Add schedule items as child tasks
          assignment.schedule.forEach(item => {
            const childId = taskId++;
            
            let taskText = "";
            let stations = "";
            
            if (item.type === "preassignment") {
              taskText = item.description;
            } else if (item.type === "flight") {
              taskText = item.flight_identifier;
              stations = `${item.departure_station} → ${item.arrival_station}`;
            }
            
            tasks.data.push({
              id: childId,
              parent: parentId,
              text: taskText,
              start_date: new Date(item.start_time),
              end_date: new Date(item.end_time),
              aircraft: assignment.aircraft,
              type: item.type,
              stations: stations,
              progress: 0
            });
          });
        });
        
        // Load data into gantt
        gantt.parse(tasks);
        setLoading(false);
        
      } catch (error) {
        console.error("Error fetching tail assignments:", error);
        setError(error.message);
        setLoading(false);
        
        // Use fallback data in case of error
        useFallbackData();
      }
    };
    
    // Fallback function to use sample data if API fails
    const useFallbackData = () => {
      // Using the sample data you provided
      const sampleData = {
        "status": "success",
        "assignments": [
          {
            "aircraft": "A320_001",
            "schedule": [
              {
                "type": "preassignment",
                "description": "Maintenance",
                "start_time": "2025-03-09T06:00:00Z",
                "end_time": "2025-03-09T07:00:00Z"
              },
              {
                "type": "flight",
                "flight_identifier": "FL001",
                "start_time": "2025-03-09T08:00:00Z",
                "end_time": "2025-03-09T16:00:00Z",
                "departure_station": "JFK",
                "arrival_station": "LHR"
              },
              {
                "type": "flight",
                "flight_identifier": "FL002",
                "start_time": "2025-03-09T18:00:00Z",
                "end_time": "2025-03-09T22:00:00Z",
                "departure_station": "LHR",
                "arrival_station": "JFK"
              }
            ]
          },
          {
            "aircraft": "B737_001",
            "schedule": [
              {
                "type": "preassignment",
                "description": "Cleaning",
                "start_time": "2025-03-09T07:00:00Z",
                "end_time": "2025-03-09T08:00:00Z"
              },
              {
                "type": "flight",
                "flight_identifier": "FL003",
                "start_time": "2025-03-09T09:00:00Z",
                "end_time": "2025-03-09T11:00:00Z",
                "departure_station": "CDG",
                "arrival_station": "FRA"
              },
              {
                "type": "flight",
                "flight_identifier": "FL004",
                "start_time": "2025-03-09T13:00:00Z",
                "end_time": "2025-03-09T15:00:00Z",
                "departure_station": "FRA",
                "arrival_station": "CDG"
              }
            ]
          },
          {
            "aircraft": "A380_001",
            "schedule": []
          },
          {
            "aircraft": "B777_001",
            "schedule": []
          }
        ]
      };
      
      // Transform data for gantt
      const tasks = {
        data: [],
        links: []
      };
      
      let taskId = 1;
      
      // Create parent tasks for each aircraft
      sampleData.assignments.forEach((assignment, index) => {
        const parentId = taskId++;
        
        // Add aircraft as parent task
        tasks.data.push({
          id: parentId,
          text: assignment.aircraft,
          aircraft: assignment.aircraft,
          type: "aircraft",
          open: true,
          render: "split" // Shows all subtasks
        });
        
        // Add schedule items as child tasks
        assignment.schedule.forEach(item => {
          const childId = taskId++;
          
          let taskText = "";
          let stations = "";
          
          if (item.type === "preassignment") {
            taskText = item.description;
          } else if (item.type === "flight") {
            taskText = item.flight_identifier;
            stations = `${item.departure_station} → ${item.arrival_station}`;
          }
          
          tasks.data.push({
            id: childId,
            parent: parentId,
            text: taskText,
            start_date: new Date(item.start_time),
            end_date: new Date(item.end_time),
            aircraft: assignment.aircraft,
            type: item.type,
            stations: stations,
            progress: 0
          });
        });
      });
      
      // Load data into gantt
      gantt.parse(tasks);
    };
    
    // Fetch data
    fetchTailAssignments();
    
    // Clean up
    return () => {
      gantt.clearAll();
      document.head.removeChild(style);
    };
  }, []);
  
  return (
    <div className="gantt-container">
      {loading && <div className="loading-overlay">Loading tail assignments...</div>}
      {error && <div className="error-message">Error: {error}</div>}
      <div 
        ref={ganttContainer} 
        style={{ width: '100%', height: '600px' }}
        className="gantt-chart-container"
      />
    </div>
  );
};

export default FlightGanttChart;
