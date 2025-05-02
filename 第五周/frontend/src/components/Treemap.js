import React, { useEffect, useState } from 'react';
import * as echarts from 'echarts';

const Treemap = () => {
  const [chartData, setChartData] = useState([]);

  const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/get_chart_data/treemap');
      const data = await response.json();
      setChartData(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    const chart = echarts.init(document.getElementById('treemap'));
    const option = {
      tooltip: { trigger: 'item' },
      series: [{
        type: 'treemap',
        data: [chartData],
        roam: false,
        label: {
          show: true,
          formatter: '{b}'
        }
      }]
    };
    chart.setOption(option);

    return () => {
      chart.dispose();
    };
  }, [chartData]);

  return (
    <div id='treemap' style={{ width: '100%', height: '80vh' }}></div>
  );
};

export default Treemap;