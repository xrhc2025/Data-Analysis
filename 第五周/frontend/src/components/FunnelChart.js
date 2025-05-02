import React, { useEffect, useState } from 'react';
import * as echarts from 'echarts';

const FunnelChart = () => {
  const [chartData, setChartData] = useState([]);

  const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/get_chart_data/funnel');
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
    const chart = echarts.init(document.getElementById('funnel-chart'));
    const option = {
      tooltip: { trigger: 'item' },
      series: [{
        type: 'funnel',
        left: '10%',
        right: '10%',
        top: '10%',
        bottom: '10%',
        min: 0,
        max: 100,
        minSize: '0%',
        maxSize: '100%',
        sort: 'descending',
        gap: 2,
        label: {
          show: true,
          position: 'inside'
        },
        labelLine: {
          length: 10,
          lineStyle: {
            width: 1,
            type: 'solid'
          }
        },
        itemStyle: {
          borderColor: '#fff',
          borderWidth: 1
        },
        emphasis: {
          label: {
            fontSize: 20
          }
        },
        data: chartData
      }]
    };
    chart.setOption(option);

    return () => {
      chart.dispose();
    };
  }, [chartData]);

  return (
    <div id='funnel-chart' style={{ width: '100%', height: '80vh' }}></div>
  );
};

export default FunnelChart;