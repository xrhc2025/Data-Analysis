import React, { useEffect, useState } from 'react';
import * as echarts from 'echarts';

const TreeChart = () => {
  const [chartData, setChartData] = useState([]);

  const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/get_chart_data/tree');
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
    const chart = echarts.init(document.getElementById('tree-chart'));
    const option = {
      tooltip: { trigger: 'item', triggerOn: 'mousemove' },
      series: [{
        type: 'tree',
        data: [chartData],
        top: '1%',
        bottom: '1%',
        layout: 'orthogonal',
        symbol: 'emptyCircle',
        symbolSize: 7,
        initialTreeDepth: -1,
        label: {
          position: 'left',
          verticalAlign: 'middle',
          align: 'right'
        },
        leaves: {
          label: {
            position: 'right',
            verticalAlign: 'middle',
            align: 'left'
          }
        },
        emphasis: {
          focus: 'descendant'
        },
        expandAndCollapse: true,
        animationDuration: 550,
        animationDurationUpdate: 750
      }]
    };
    chart.setOption(option);

    return () => {
      chart.dispose();
    };
  }, [chartData]);

  return (
    <div id='tree-chart' style={{ width: '100%', height: '80vh' }}></div>
  );
};

export default TreeChart;