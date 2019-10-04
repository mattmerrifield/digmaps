import React, {useRef} from 'react';
import ReactMapGL, {Marker, NavigationControl, ViewState} from 'react-map-gl';
import {ReactNode, useEffect, useState} from "react";
import {BoxProps, Text, Box, Flex} from "rebass";
import {TLengthStyledSystem} from "styled-system";
import InteractiveMap from "react-map-gl";
import {FaMapMarker} from "react-icons/fa";
import {useSitesQuery} from "./generated/graphql";

const MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN || '';


// interface State {
//     viewport: ViewState
// }

interface SiteMarkerProps{
 site: {
    modernName?: string
    coordinates: {
        x: number
        y: number
    }
}}

const SiteMarker = (props: SiteMarkerProps): React.ReactNode => {

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

interface SitesMarkerProps {
    x1: number
    y1: number
    x2: number
    y2: number

}

const SitesMarkers = (props: SitesMarkerProps) => {

    const {x1, y1, x2, y2 } = props;
    const rect = `(${x1}, ${y1}), (${x2}, ${y2}`;
    const {data, loading, error} = useSitesQuery({variables: {rect: rect, limit: 10000}});

    if (data && data.sites) {
        return <>{data.sites.map(
            (site, i) => {
                return <SiteMarker key={i} site={site}/>
            }
        ).filter(
            (element, i) => element
        )}</>
    }
    else {
        return <></>
    }
};



interface NavLocation {
    top?: number
    bottom?: number
    left?: number
    right?: number
}

interface MapProps extends BoxProps {
    children?: ReactNode
    width?: TLengthStyledSystem
    height?: TLengthStyledSystem
    navLocation?: NavLocation
}



const Map = (props: MapProps) => {
    // A dynamically resizing, flexbox-compatible map widget!

    const navLocation = props.navLocation || {bottom: 30, right: 30};

    const initialState = {
        viewport: {
            latitude: 31.7683,
            longitude: 35.2137,
            zoom: 8,
            height: props.height || '100%',
            width: props.width || '100%'
        },
    };

    type State = typeof initialState
    const [state, setState] = useState<State>(initialState);
    const divRef = useRef<HTMLDivElement>(null);
    const mapRef = useRef<InteractiveMap>(null);

    // Pass in a function to execute when the component finishes mounting
    const componentDidMount = () => {
        const divHeight = () => {
            if (divRef && divRef.current) {
                return divRef.current.clientHeight
            }
        };

        const divWidth = () => {
            if (divRef && divRef.current) {
                return divRef.current.clientWidth
            }
        };

        const resize = () => {
            setState(prevState => ({
                viewport: {
                    ...prevState.viewport,
                    height: divHeight() || initialState.viewport.height,
                    width: divWidth() || initialState.viewport.width,
                },
            }));
        };
        window.addEventListener('resize', resize);
        resize();
        // Return from the first function argument another function, which will be called during unmount
        return () => window.removeEventListener('resize', resize);
    };

    useEffect(
        // Register the resize event listener with useEffect
        componentDidMount,
        // Second argument is an empty list => execute first argument only after monunting
        // not every time!
        []
    );

    // Update the viewport whenever we scroll or click on a nav control
    const updateViewport = (viewport: ViewState) => {
        setState(prevState => ({
            viewport: { ...prevState.viewport, ...viewport },
        }));
    };

    const getBounds = () => {
        if (mapRef.current) {
            const bounds = mapRef.current.getMap().getBounds();
            return {x1: bounds.getEast(), y1: bounds.getNorth(), x2: bounds.getWest(), y2: bounds.getSouth()};
        }
        else
            {
                return {x1: 0, y1: 0, x2: 0, y2: 0}

            }
    };


    return (
        <div ref={divRef}>
            <ReactMapGL
                {...state.viewport}
                mapboxApiAccessToken={MAPBOX_TOKEN}
                onViewportChange={(v: ViewState) => updateViewport(v)}
                ref={mapRef}
            >
                <div style={{ position: 'absolute', ...navLocation }}>
                   <NavigationControl onViewportChange={updateViewport} />
                </div>
                <SitesMarkers {...getBounds()}/>
                {props.children}
            </ReactMapGL>
        </div>
    );
};

export default Map;