import MissileDashboard from "./MissileDashboard"
import { useState, useEffect } from 'react';
import "./App.css"

function Radar() { 
    const [isMissle, setDetected] = useState(true);
    return(<div class="Radar"><MissileDashboard/></div>)

}