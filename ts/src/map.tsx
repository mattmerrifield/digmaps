/** @jsx jsx */
import React, {useRef} from 'react';
import { jsx } from "@emotion/core";
import ReactMapGL, {Marker, NavigationControl, ViewState} from 'react-map-gl';
import {ReactNode, useEffect, useState, useCallback} from "react";
import {BoxProps, Text, Box, Flex} from "rebass";
import {TLengthStyledSystem} from "styled-system";
import InteractiveMap from "react-map-gl";
import {FaMapMarker} from "react-icons/fa";
import {useSitesQuery} from "./generated/graphql";
import {ViewportChangeHandler} from "react-map-gl"
import MapboxGL from 'mapbox-gl';
import {debounce} from "lodash";
import {Bounds} from "viewport-mercator-project";


const MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN || '';


// interface State {
//     viewport: ViewState
// }

interface SiteMarkerProps{
 site: {
    modernName: string
    coordinates: {
        x: number
        y: number
    }
}}

const SiteMarker: React.FC<SiteMarkerProps> = (props) => {

    const [name, setName] = useState(<></>);

    const showName = () => setName(<Text>{props.site.modernName}</Text>);
    const hideName = () => setName(<></>);

    return (
        <Marker latitude={props.site.coordinates.y} longitude={props.site.coordinates.x}>
            <FaMapMarker onMouseEnter={showName} onMouseLeave={hideName}/>
            {name}
        </Marker>
    )

};

const getBounds = (map: MapboxGL.Map): Bounds => {
    const bounds = map.getBounds();
    return [[bounds.getEast(),  bounds.getNorth()], [bounds.getWest(), bounds.getSouth()]];
};

interface SitesMarkersProps {
    bounds: Bounds
}

const SitesMarkers: React.FC<SitesMarkersProps> = (props) => {

    const [[south, west], [north, east]] = props.bounds;
    const rect = `(${west}, ${north}), (${east}, ${south}`;
    const {data, loading, error} = useSitesQuery({variables: {rect: rect, limit: 10000}});

    if (data && data.sites) {
        return <React.Fragment>{data.sites.map(
              (site, i) => {
                    return <SiteMarker key={i} site={site}/>
              }
          ).filter(
              (element, i) => element )}
        </React.Fragment>
    }
    else {
        return null;
    }
};



interface NavLocation {
    top?: number
    bottom?: number
    left?: number
    right?: number
}



interface MapProps extends BoxProps {
    navLocation: NavLocation
}


const Map: React.FC<MapProps> & {defaultProps: Partial<MapProps>} = (props) => {
    // A dynamically resizing, flexbox-compatible map widget!
    const [viewport, setViewport] = useState<ViewState>({latitude: 31.7683, longitude: 35.2137, zoom: 8});
    const [bounds, setBounds] = useState<Bounds>([[0,0], [0,0]]);
    const [height, setHeight] = useState<string | number>('100%');
    const [width, setWidth] = useState<string | number>( '100%');
    const divRef = useRef<HTMLDivElement>(null);
    const mapRef = useRef<InteractiveMap>(null);


    useEffect(
      // Register the resize event listener with useEffect
     () => {
        const resize = () => {
            if (divRef && divRef.current && divRef.current.clientHeight) {
                setHeight(divRef.current.clientHeight);
            }
            if (divRef && divRef.current && divRef.current.clientWidth) {
                setWidth(divRef.current.clientWidth);
            }
        };
        window.addEventListener('resize', resize);
        resize();
        // Return from the first function argument another function, which will be called during unmount
        return () => window.removeEventListener('resize', resize);
    },
        // Second argument is an empty list => execute first argument only after monunting
        // not every time!
        []
    );

    // Update the viewport whenever we scroll or click on a nav control
    const updateViewport: ViewportChangeHandler = (viewport) => {
        setViewport(viewport);
        if (mapRef.current) {
            const map = mapRef.current.getMap();
            setBounds(getBounds(map));
        }
    };


    return (
        <Flex height="100%" flexDirection="column" ref={divRef}>
            <ReactMapGL
                {...viewport}
                width={width}
                height={height}
                mapboxApiAccessToken={MAPBOX_TOKEN}
                onViewportChange={(v: ViewState) => updateViewport(v)}
                ref={mapRef}
                css={{
                    flex: "1 0 auto"
                }}
            >
                <div style={{ position: 'absolute', ...props.navLocation }}>
                   <NavigationControl onViewportChange={updateViewport} />
                </div>
                {}
                <SitesMarkers bounds={bounds}/>
                {props.children}
           </ReactMapGL>
        </Flex>
    );
};

Map.defaultProps = {
    height: "100%",
    width: "100%",
    navLocation: {
        bottom: 30,
        right: 30,
    }
};

export default Map;