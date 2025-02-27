// dashboard/src/components/Dashboard.js
import React from 'react';
import EventChart from './EventChart';
import UserActivityChart from './UserActivityChart';

function Dashboard() {
    return (
        <div>
            <h2>Dashboard</h2>
            <EventChart />
            <UserActivityChart />
        </div>
    );
}

export default Dashboard;