// App.js or MissileDashboard.js

import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { useState, useEffect } from 'react';
import 'leaflet/dist/leaflet.css';

function MissileDashboard() {
  const [position, setPosition] = useState([22.5937, 78.9629]); // Start in India

  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate random missile movement
      setPosition(prevPos => {
        const randomLat = prevPos[0] + (Math.random() - 0.5) * 0.2;  // move slightly
        const randomLng = prevPos[1] + (Math.random() - 0.5) * 0.2;
        return [randomLat, randomLng];
      });
    }, 1000); // Update every 1 second

    return () => clearInterval(interval);
  }, []);

  return (
    <MapContainer center={position} zoom={5} style={{ height: "100vh", width: "100%" }}>
  <TileLayer
    url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
    attribution="&copy; OpenStreetMap contributors & CartoDB"
  />
  <Marker position={position}>
    <Popup>Missile in Motion!</Popup>
  </Marker>
</MapContainer>

  );
}

export default MissileDashboard;
