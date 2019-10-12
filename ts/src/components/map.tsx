/** @jsx jsx */
import React, {useEffect, useRef, useState} from 'react';
import {jsx} from "@emotion/core";
import ReactMapGL from 'react-map-gl';
import InteractiveMap, {NavigationControl, ViewportChangeHandler, ViewState} from 'react-map-gl';
import {BoxProps, Flex} from "rebass";
import {Bounds} from "viewport-mercator-project";


const MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN || '';


// interface State {
//     viewport: ViewState
// }



interface NavLocation {
    top?: number
    bottom?: number
    left?: number
    right?: number
}

interface MapBounds {
    east: number
    north: number
    south: number
    west: number
}


const nullIsland: MapBounds = {
    north: 0,
    south: 0,
    east: 0,
    west: 0,
};



interface MapProps extends BoxProps {
    navLocation: NavLocation
    viewport: ViewState
    render: (bounds: MapBounds) => React.ReactElement
}


// A dynamically resizing, flexbox-compatible map widget!
const Map: React.FC<MapProps> & {defaultProps: Partial<MapProps>} = (props) => {
    const [viewport, setViewport] = useState<ViewState>(props.viewport);
    const [bounds, setBounds] = useState<MapBounds>(nullIsland);
    const [height, setHeight] = useState<string | number>('100%');
    const [width, setWidth] = useState<string | number>( '100%');
    const divRef = useRef<HTMLDivElement>(null);
    const mapRef = useRef<InteractiveMap>(null);


    // Register the resize event listener when the map first mounts
    useEffect(
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

        // run at mount to initialize screen
        resize();
        updateBounds(viewport);

        // Return from the first function argument another function, which will be called during unmount
        return () => window.removeEventListener('resize', resize);
    },
        // Second argument is an empty list, so we execute first argument only after monunting, and never again
        // not every time!
        []
    );

    // Update the viewport whenever we scroll or click on a nav control
    const updateBounds: ViewportChangeHandler = (viewport: ViewState) => {
        setViewport(viewport);
        if (mapRef.current) {
            const bounds = mapRef.current.getMap().getBounds();
            setBounds({
                east: bounds.getEast(),
                north: bounds.getNorth(),
                west: bounds.getWest(),
                south: bounds.getSouth()
            })
        }
    };


    return (
        <Flex height="100%" flexDirection="column" ref={divRef}>
            <ReactMapGL
                {...viewport}
                width={width}
                height={height}
                mapboxApiAccessToken={MAPBOX_TOKEN}
                onViewportChange={updateBounds}
                ref={mapRef}
                css={{
                    flex: "1 0 auto"
                }}
            >
                <div style={{ position: 'absolute', ...props.navLocation }}>
                   <NavigationControl onViewportChange={updateBounds} />
                   {props.render(bounds)}
                </div>
           </ReactMapGL>
        </Flex>
    );
};

Map.defaultProps = {
    navLocation: {
        bottom: 30,
        right: 30,
    },
    viewport: {latitude: 31.7683, longitude: 35.2137, zoom: 8}
};

export default Map;