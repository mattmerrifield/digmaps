import React, {useRef} from 'react';
import ReactMapGL, {NavigationControl, ViewState} from 'react-map-gl';
import {ReactNode, useEffect, useState} from "react";
import {BoxProps, Text, Box, Flex} from "rebass";
import {TLengthStyledSystem} from "styled-system";
import {Query} from "react-apollo";
import {Sites, SitesVariables} from "./queries/types/Sites";
import siteQuery from "./queries/siteQuery";

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

interface MapProps extends BoxProps {
    children?: ReactNode
    width?: TLengthStyledSystem
    height?: TLengthStyledSystem
    navLocation?: NavLocation
}


class SiteQuery extends Query<Sites, SitesVariables> {}

const SitesMarkers = () => {
    return (
      <SiteQuery
        query={siteQuery}
        variables={{limit: 10}}
      >
        {({ data: Sites }) => (
          <>
          </>
         )}
      </SiteQuery>
    )
};


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

    // Register the resize event listener with useEffect
    useEffect(
        // Pass in a function to execute when the component finishes mounting
        () => {
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
        },
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


    return (
        <div ref={divRef}>
            <ReactMapGL
                {...state.viewport}
                mapboxApiAccessToken={MAPBOX_TOKEN}
                onViewportChange={(v: ViewState) => updateViewport(v)}
            >
                <div style={{ position: 'absolute', ...navLocation }}>
                   <NavigationControl onViewportChange={updateViewport} />
                </div>
                {props.children}
            </ReactMapGL>
        </div>
    );
};

export default Map;