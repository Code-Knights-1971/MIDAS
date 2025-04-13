import "./index.css"
import img from "./images/missile.png"
import red from "./images/red dot.png"
import green from "./images/green dot.png"
import satGreen from "./images/satellite.png"
import satred from "./images/satellite red.png"
import {useState,useEffect} from "react"

function Header() { 
    const [headerCont, setHeadCont] = useState({});
   
    return (<div className="header">
        <div className="header">
            <div className="logo">
                <img src={img} alt="logo" />
                <div className="logo-content">
                    <p style={{ fontSize: 10 , "font-family": "'Orbitron', monospace"}}>M . I . D . A . S</p>
                    <p id="description">Missile Interception Decision Analysis System</p>

                </div>
            </div>
            <div className="sideCont">
                <SystemStatus />
                <SatelliteStatus />
                <RealTimeClockWithDate />
            </div>
            
        </div>
    
    </div>)
    


}

function SystemStatus() { 
    const [operationalStatus, setStatus] = useState(false);

  return (
    <div className="operationalSts">
      {operationalStatus ? (
        <img src={green} alt="success" />
      ) : (
        <img src={red} alt="failure" />
      )}
      <p>SYSTEM OPERATIONAL</p>
    </div>
  );
}
function RealTimeClockWithDate() {
    const [time, setTime] = useState('');
    const [date, setDate] = useState('');
  
    useEffect(() => {
      const timer = setInterval(() => {
        const now = new Date();
  
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const month = String(now.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
        const year = now.getFullYear();
  
        setTime(`${hours}.${minutes}.${seconds}`);
        setDate(`${day}/${month}/${year}`);
      }, 1000);
  
      return () => clearInterval(timer); // clean up
    }, []);
  
    return (
      <div style={{ 
        fontFamily: "'Courier New', Courier, monospace", 
        fontSize: '2rem', 
        color: 'white', 
            textAlign: 'center',
            display: "flex",
            alignItems: "center",
            gap:"10px",
            fontSize: "10px"
      }}>
            <div>{time}</div>
        <div style={{ fontSize: '10px',color:"aqua" }}>{date}</div>
      </div>
    );
}
function SatelliteStatus() {
    const [satelliteConnected, setSatelliteConnected] = useState(false);
  
    return (
      <div className="satelliteSts">
        {satelliteConnected ? (
          <img src={satGreen} alt="connected" />
        ) : (
          <img src={satred} alt="disconnected" />
        )}
      </div>
    );
  }

export default Header