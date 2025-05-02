import React, { useEffect, useState } from 'react';
import * as echarts from 'echarts';

const SunburstChart = () => {
  const [chartData, setChartData] = useState([]);

  const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/get_chart_data/sunburst');
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
    const chart = echarts.init(document.getElementById('sunburst-chart'));
    const option = {
      tooltip: { trigger: 'item' },
      series: [{
        type: 'sunburst',
        data: [chartData],
        radius: [0, '90%'],
        label: {
          rotate: 'radial'
        }
      }]
    };
    chart.setOption(option);

    return () => {
      chart.dispose();
    };
  }, [chartData]);

  return (
    <div id='sunburst-chart' style={{ width: '100%', height: '80vh' }}></div>
  );
};

export default SunburstChart;