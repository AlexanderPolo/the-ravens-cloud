from http.server import BaseHTTPRequestHandler
import json
import math

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Отримуємо дані з тіла запиту
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        # Та сама логіка розрахунку, що й раніше
        try:
            BATTERY_VOLTAGE = 25.2
            USABLE_BATTERY_CAPACITY = 1.0
            HOVER_POWER_COEFFICIENT = 200
            CRUISE_SPEED_CALIBRATION = 15

            total_weight_kg = data['droneWeight'] + data['payloadWeight'] + data['batteryWeight']
            battery_capacity_ah = data['batteryCapacityMAh'] / 1000
            total_energy_wh = battery_capacity_ah * BATTERY_VOLTAGE
            usable_energy_wh = total_energy_wh * USABLE_BATTERY_CAPACITY
            power_hover_w = total_weight_kg * HOVER_POWER_COEFFICIENT
            drag_coefficient = power_hover_w / (CRUISE_SPEED_CALIBRATION ** 3)
            drone_angle_rad = math.radians(data['droneAngle_deg'])
            wind_angle_rad = math.radians(data['windAngle_deg'])
            drone_vx = data['groundSpeed_ms'] * math.sin(drone_angle_rad)
            drone_vy = -data['groundSpeed_ms'] * math.cos(drone_angle_rad)
            wind_vx = data['windSpeed_ms'] * math.sin(wind_angle_rad)
            wind_vy = -data['windSpeed_ms'] * math.cos(wind_angle_rad)
            air_speed_vx = drone_vx - wind_vx
            air_speed_vy = drone_vy - wind_vy
            air_speed_ms = math.sqrt(air_speed_vx**2 + air_speed_vy**2)
            power_drag_w = drag_coefficient * (air_speed_ms ** 3)
            total_power_w = power_hover_w + power_drag_w
            flight_time_h = usable_energy_wh / total_power_w
            flight_time_min = flight_time_h * 60
            flight_distance_m = data['groundSpeed_ms'] * (flight_time_h * 3600)
            flight_distance_km = flight_distance_m / 1000

            result = {
                'flightDistance_km': round(flight_distance_km, 2),
                'flightTime_min': round(flight_time_min, 1),
                'airSpeed_ms': round(air_speed_ms, 1),
                'totalPower_W': round(total_power_w, 0)
            }

            # Відправляємо успішну відповідь
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))

        except Exception as e:
            # Відправляємо відповідь з помилкою
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

        return