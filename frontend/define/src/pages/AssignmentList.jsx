import React from 'react';

const AssignmentList = ({ assignments }) => {
    return (
        <div>
            <h1>Assignments</h1>
            <ul>
                {assignments.map(assignment => (
                    <li key={assignment.id}>
                        Flight {assignment.flight_id} assigned to Aircraft {assignment.aircraft_id} on {assignment.assigned_date}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default AssignmentList;