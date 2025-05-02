from flask import Blueprint, jsonify
import random
import json

chart_bp = Blueprint('chart', __name__)


@chart_bp.route('/get_chart_data/<chart_type>', methods=['GET'])
def get_chart_data(chart_type):
    if chart_type == 'pie':
        data = [{'name': 'A', 'value': random.randint(10, 100)},
                {'name': 'B', 'value': random.randint(10, 100)},
                {'name': 'C', 'value': random.randint(10, 100)}]
    elif chart_type == 'bar':
        data = [{'name': 'X', 'value': random.randint(10, 100)},
                {'name': 'Y', 'value': random.randint(10, 100)},
                {'name': 'Z', 'value': random.randint(10, 100)}]
    elif chart_type == 'line':
        data = [{'name': str(i), 'value': random.randint(10, 100)} for i in range(10)]
    elif chart_type == 'china_map':
        try:
            import os
            file_path = os.path.join(os.path.dirname(__file__), 'china_map_data.json')
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    elif chart_type == 'graph':
        nodes = [{'name': f'Node {i}'} for i in range(10)]
        links = [{'source': random.randint(0, 9), 'target': random.randint(0, 9)} for _ in range(15)]
        data = {'nodes': nodes, 'links': links}
    elif chart_type == 'scatter':
        data = [[random.randint(0, 100), random.randint(0, 100)] for _ in range(50)]
    elif chart_type == 'radar':
        data = [{'value': [random.randint(0, 100) for _ in range(5)], 'name': 'Data'}]
    elif chart_type == 'path':
        data = [[random.randint(0, 100), random.randint(0, 100)] for _ in range(10)]
    elif chart_type == 'k_line':
        data = [{'name': str(i), 'value': [random.randint(10, 100), random.randint(10, 100), random.randint(10, 100), random.randint(10, 100)]} for i in range(10)]
    elif chart_type == 'heat_map':
        xAxisData = [f'x{i}' for i in range(10)]
        yAxisData = [f'y{i}' for i in range(10)]
        valueData = [[i, j, random.randint(0, 100)] for i in range(10) for j in range(10)]
        data = {'xAxisData': xAxisData, 'yAxisData': yAxisData, 'valueData': valueData}
    elif chart_type == 'tree':
        data = {
            'name': 'Root',
            'children': [
                {'name': 'Child1', 'children': [{'name': 'GrandChild1'}, {'name': 'GrandChild2'}]},
                {'name': 'Child2', 'children': [{'name': 'GrandChild3'}]}
            ]
        }
    elif chart_type == 'treemap':
        data = {
            'name': 'Root',
            'children': [
                {'name': 'Child1', 'value': 100},
                {'name': 'Child2', 'value': 200},
                {'name': 'Child3', 'value': 300}
            ]
        }
    elif chart_type == 'sunburst':
        data = {
            'name': 'Root',
            'children': [
                {'name': 'Child1', 'value': 100},
                {'name': 'Child2', 'value': 200},
                {'name': 'Child3', 'value': 300}
            ]
        }
    elif chart_type == 'sankey':
        nodes = [{'name': 'Node1'}, {'name': 'Node2'}, {'name': 'Node3'}]
        links = [{'source': 'Node1', 'target': 'Node2', 'value': 100}, {'source': 'Node2', 'target': 'Node3', 'value': 200}]
        data = {'nodes': nodes, 'links': links}
    elif chart_type == 'funnel':
        data = [{'name': 'Step1', 'value': 100}, {'name': 'Step2', 'value': 80}, {'name': 'Step3', 'value': 60}]
    elif chart_type == 'pictorial_bar':
        data = [{'name': 'A', 'value': 100}, {'name': 'B', 'value': 200}, {'name': 'C', 'value': 300}]
    else:
        data = []
    return jsonify(data)