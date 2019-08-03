/* tslint:disable */
/* eslint-disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: Sites
// ====================================================

export interface Sites_sites_coordinates {
  __typename: "PointFieldType";
  x: number;
  y: number;
}

export interface Sites_sites {
  __typename: "SiteType";
  /**
   * Django object unique identification field
   */
  id: string;
  /**
   * Name used by modern peoples
   */
  modernName: string | null;
  /**
   * Name used by ancient peoples
   */
  ancientName: string | null;
  coordinates: Sites_sites_coordinates;
}

export interface Sites {
  /**
   * Site list
   */
  sites: (Sites_sites | null)[] | null;
}

export interface SitesVariables {
  limit: number;
}
