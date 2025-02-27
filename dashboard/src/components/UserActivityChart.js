// dashboard/src/components/UserActivityChart.js
import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import axios from 'axios';

function UserActivityChart() {
    const [data, setData] = useState([]);

    useEffect(() => {
        axios.get('/api/v1/reports?date_from=2025-02-20&date_to=2025-02-27&group_by=user_id')
            .then(response => setData(response.data))
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    return (
        <BarChart width={600} height={300} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="user_id" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="count" fill="#82ca9d" />
        </BarChart>
    );
}

export default UserActivityChart;