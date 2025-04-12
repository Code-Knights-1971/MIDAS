import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { useState, useEffect } from 'react';
import axios from 'axios';

function MissileDashboard() {
  const [position, setPosition] = useState([22.5937, 78.9629]); // India coords
  const [speed, setSpeed] = useState(null);
  const [threatLevel, setThreatLevel] = useState('');

  useEffect(() => {
    const interval = setInterval(() => {
      axios.get('http://localhost:8080/api/missile-data', {
        auth: {
          username: 'admin',
          password: 'securepass'
        }
      })
      .then(response => {
        const data = response.data;
        if (data && data.latitude && data.longitude) {
          setPosition([data.latitude, data.longitude]);
          setSpeed(data.speed);
          setThreatLevel(data.threatLevel);
        }
      })
      .catch(error => {
        console.error('Error fetching missile data:', error);
      });
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <MapContainer center={position} zoom={5} style={{ height: '100vh', width: '100%' }}>
      <TileLayer
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
      <Marker position={position}>
        <Popup>
          🚀 Missile in Motion! <br />
          Speed: {speed ? `${speed} m/s` : 'Loading...'} <br />
          Threat Level: {threatLevel || 'Loading...'}
        </Popup>
      </Marker>
    </MapContainer>
  );
}

export default MissileDashboard;

