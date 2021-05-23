import logo from "./logo.svg";
import "./App.css";

import React from "react";
import { MapContainer, TileLayer, Marker, Tooltip } from "react-leaflet";

class Map extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      areCachesLoaded: false,
      areUsersLoaded: false,
      caches: [],
      users: [],
    };
  }

  componentDidMount() {
    fetch("http://192.168.0.70:5000/caches")
      .then((res) => res.json())
      .then((result) => {
        this.setState({
          caches: result.caches,
          areCachesLoaded: true,
        });
      });
    fetch("http://192.168.0.70:5000/users")
      .then((res) => res.json())
      .then((result) => {
        this.setState({
          users: result.users,
          areUsersLoaded: true,
        });
      });
  }

  render() {
    const { areCachesLoaded, areUsersLoaded, caches, users } = this.state;
    if (!areCachesLoaded || !areUsersLoaded) {
      return <div>Loading...</div>;
    } else {
      return (
        <MapContainer
          id="mapid"
          center={[caches[0].lat, caches[0].lon]}
          zoom={13}
        >
          <TileLayer
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {caches.map((cache) => (
            <Marker position={{ lat: cache.lat, lon: cache.lon }}>
              <Tooltip>
                <span style={{ fontSize: 16 }}>
                  <b>{cache.name}</b>
                </span>
                <br />
                {cache.created_at}
                <br />
                <br />
                <b>Owner: </b>
                {users[cache.owner_id - 1].name}
                <br />
                <b>Description: </b>
                <br />
                {cache.description.split("\n").map((i, key) => {
                  return <div key={key}>{i}</div>;
                })}
              </Tooltip>
            </Marker>
          ))}
        </MapContainer>
      );
    }
  }
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default Map;
