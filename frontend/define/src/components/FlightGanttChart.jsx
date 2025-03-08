import React, { useEffect, useRef } from "react";
import "dhtmlx-gantt/codebase/dhtmlxgantt.css";
import { gantt } from "dhtmlx-gantt";

const FlightGanttChart = () => {
  const ganttContainer = useRef(null);

  useEffect(() => {
    // Configure gantt
    gantt.config.date_format = "%Y-%m-%d %H:%i";
    gantt.config.scale_unit = "day";
    gantt.config.date_scale = "%d %M";
    gantt.config.subscales = [
      { unit: "hour", step: 6, date: "%H:%i" }
    ];
    gantt.config.columns = [
      { name: "text", label: "Flight", tree: true, width: 200 },
      { name: "start_date", label: "Departure", align: "center", width: 120 },
      { name: "aircraft", label: "Aircraft", align: "center", width: 80 }
    ];

    // Initialize gantt
    gantt.init(ganttContainer.current);

    // Fetch data or use sample data
    const fetchFlightData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/flights/");
        
        if (!response.ok) {
          throw new Error("Failed to fetch flight data");
        }
        
        const data = await response.json();
        
        // Transform API data to gantt format
        const tasks = data.map((flight, index) => ({
          id: flight.id || index + 1,
          text: flight.flight_number || `Flight ${index + 1}`,
          start_date: new Date(flight.flight_datetime).toISOString().slice(0, 16).replace('T', ' '),
          duration: 3, // Default 3 hours duration
          aircraft: flight.aircraft_id || "Unknown"
        }));

        // Load data into gantt
        gantt.parse({ data: tasks, links: [] });
        
      } catch (error) {
        console.error("Error fetching flight data:", error);
        
        // Fallback to sample data
        const sampleTasks = [
          { id: 1, text: "Flight AA123", start_date: "2025-03-10 08:00", duration: 3, aircraft: "B737-1" },
          { id: 2, text: "Flight AA456", start_date: "2025-03-11 09:30", duration: 2, aircraft: "A320-1" },
          { id: 3, text: "Flight AA789", start_date: "2025-03-12 14:00", duration: 4, aircraft: "B787-1" },
          { id: 4, text: "Flight AA234", start_date: "2025-03-13 10:15", duration: 3, aircraft: "B747-1" },
          { id: 5, text: "Flight AA567", start_date: "2025-03-14 16:45", duration: 2, aircraft: "A380-1" }
        ];
        
        // Load sample data into gantt
        gantt.parse({ data: sampleTasks, links: [] });
      }
    };

    fetchFlightData();

    // Clean up
    return () => {
      gantt.clearAll();
    };
  }, []);

  return (
    <div 
      ref={ganttContainer} 
      style={{ width: '100%', height: '400px' }}
      className="gantt-chart-container"
    />
  );
};

export default FlightGanttChart;
