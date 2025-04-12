import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { useState, useEffect } from 'react';
import axios from 'axios';
import "./App.css"
import 'leaflet/dist/leaflet.css';

function MissileDashboard() {
  const [position, setPosition] = useState([22.5937, 78.9629]); // Default starting point (India)

  useEffect(() => {
    const fetchMissilePosition = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8080/api/missile-data', {
          auth: {
            username: 'admin',
            password: 'aa',
          },
        });

        const { lat, lng } = response.data;
        setPosition([lat, lng]);
      } catch (error) {
        console.error('Error fetching missile position:', error);
      }
    };

    // Fetch every second
    const interval = setInterval(fetchMissilePosition, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className='radar' style={{ width: '500px', height: '500px' }}>
    <MapContainer center={position} zoom={3} style={{ height: "100%", width: "100%" }}>
      <TileLayer
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        attribution="&copy; OpenStreetMap contributors & CartoDB"
      />
      <Marker position={position}>
        <Popup>Missile in Motion!</Popup>
      </Marker>
      </MapContainer>
      </div>
  );
}

export default MissileDashboard;
