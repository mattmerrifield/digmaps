import gql from "graphql-tag";
import * as React from "react";
import * as ReactApollo from "react-apollo";
import * as ReactApolloHooks from "react-apollo-hooks";
export type Maybe<T> = T | null;
export type Omit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
};

export type Derp = {
  __typename?: "Derp";
  ok?: Maybe<Scalars["Boolean"]>;
};

export type FeatureType = {
  __typename?: "FeatureType";
  /** description */
  description?: Maybe<Scalars["String"]>;
  /** Django object unique identification field */
  id: Scalars["ID"];
  /** name */
  name?: Maybe<Scalars["String"]>;
  /** shortname */
  shortname?: Maybe<Scalars["String"]>;
  sitefeature?: Maybe<Array<Maybe<SiteFeatureType>>>;
  /** Site list */
  sites?: Maybe<Array<Maybe<SiteType>>>;
};

export type FeatureTypeSitesArgs = {
  id?: Maybe<Scalars["Float"]>;
  code?: Maybe<Scalars["String"]>;
  code_Icontains?: Maybe<Scalars["String"]>;
  region_Id?: Maybe<Scalars["Float"]>;
  region_Name?: Maybe<Scalars["String"]>;
  region_Name_Icontains?: Maybe<Scalars["String"]>;
  modernName_Icontains?: Maybe<Scalars["String"]>;
  ancientName_Icontains?: Maybe<Scalars["String"]>;
  area_Lt?: Maybe<Scalars["Float"]>;
  area_Gt?: Maybe<Scalars["Float"]>;
};

export type Mutation = {
  __typename?: "Mutation";
  derp?: Maybe<Derp>;
};

export type MutationDerpArgs = {
  name?: Maybe<Scalars["String"]>;
};

export type PeriodType = {
  __typename?: "PeriodType";
  /** description */
  description?: Maybe<Scalars["String"]>;
  /** Approximate Ending (BCE is negative) */
  end?: Maybe<Scalars["Int"]>;
  /** Django object unique identification field */
  id: Scalars["ID"];
  /** name */
  name?: Maybe<Scalars["String"]>;
  /** Unique code name, e.g. 'EBIV' */
  shortname?: Maybe<Scalars["String"]>;
  sitefeature?: Maybe<Array<Maybe<SiteFeatureType>>>;
  /** Site list */
  sites?: Maybe<Array<Maybe<SiteType>>>;
  /** Approximate Beginning (BCE is negative) */
  start?: Maybe<Scalars["Int"]>;
};

export type PeriodTypeSitesArgs = {
  id?: Maybe<Scalars["Float"]>;
  code?: Maybe<Scalars["String"]>;
  code_Icontains?: Maybe<Scalars["String"]>;
  region_Id?: Maybe<Scalars["Float"]>;
  region_Name?: Maybe<Scalars["String"]>;
  region_Name_Icontains?: Maybe<Scalars["String"]>;
  modernName_Icontains?: Maybe<Scalars["String"]>;
  ancientName_Icontains?: Maybe<Scalars["String"]>;
  area_Lt?: Maybe<Scalars["Float"]>;
  area_Gt?: Maybe<Scalars["Float"]>;
};

/** An extremely simple representation of a single coordinate */
export type PointFieldType = {
  __typename?: "PointFieldType";
  x: Scalars["Float"];
  y: Scalars["Float"];
};

/** Leverage multiple inheritance to expose each module's query fields as top-level fields */
export type Query = {
  __typename?: "Query";
  /** Site list */
  sites?: Maybe<Array<Maybe<SiteType>>>;
  /** Region list */
  regions?: Maybe<Array<Maybe<RegionType>>>;
  /** SiteFeature list */
  siteFeatures?: Maybe<Array<Maybe<SiteFeatureType>>>;
  /** Feature list */
  features?: Maybe<Array<Maybe<FeatureType>>>;
};

/** Leverage multiple inheritance to expose each module's query fields as top-level fields */
export type QuerySitesArgs = {
  id?: Maybe<Scalars["Float"]>;
  code?: Maybe<Scalars["String"]>;
  code_Icontains?: Maybe<Scalars["String"]>;
  region_Id?: Maybe<Scalars["Float"]>;
  region_Name?: Maybe<Scalars["String"]>;
  region_Name_Icontains?: Maybe<Scalars["String"]>;
  modernName_Icontains?: Maybe<Scalars["String"]>;
  ancientName_Icontains?: Maybe<Scalars["String"]>;
  area_Lt?: Maybe<Scalars["Float"]>;
  area_Gt?: Maybe<Scalars["Float"]>;
  limit?: Maybe<Scalars["Int"]>;
  offset?: Maybe<Scalars["Int"]>;
  ordering?: Maybe<Scalars["String"]>;
};

/** Leverage multiple inheritance to expose each module's query fields as top-level fields */
export type QueryRegionsArgs = {
  id?: Maybe<Scalars["Float"]>;
  name?: Maybe<Scalars["String"]>;
  name_Icontains?: Maybe<Scalars["String"]>;
  description_Icontains?: Maybe<Scalars["String"]>;
  limit?: Maybe<Scalars["Int"]>;
  offset?: Maybe<Scalars["Int"]>;
  ordering?: Maybe<Scalars["String"]>;
};

/** Leverage multiple inheritance to expose each module's query fields as top-level fields */
export type QuerySiteFeaturesArgs = {
  site?: Maybe<Scalars["ID"]>;
  feature?: Maybe<Scalars["ID"]>;
  evidence?: Maybe<Scalars["String"]>;
  periods?: Maybe<Array<Maybe<Scalars["ID"]>>>;
  id?: Maybe<Scalars["ID"]>;
  limit?: Maybe<Scalars["Int"]>;
  offset?: Maybe<Scalars["Int"]>;
  ordering?: Maybe<Scalars["String"]>;
};

/** Leverage multiple inheritance to expose each module's query fields as top-level fields */
export type QueryFeaturesArgs = {
  shortname?: Maybe<Scalars["String"]>;
  name?: Maybe<Scalars["String"]>;
  description?: Maybe<Scalars["String"]>;
  id?: Maybe<Scalars["ID"]>;
  limit?: Maybe<Scalars["Int"]>;
  offset?: Maybe<Scalars["Int"]>;
  ordering?: Maybe<Scalars["String"]>;
};

export type RegionType = {
  __typename?: "RegionType";
  /** description */
  description?: Maybe<Scalars["String"]>;
  /** Django object unique identification field */
  id: Scalars["ID"];
  /** name */
  name?: Maybe<Scalars["String"]>;
  /** Site list */
  site?: Maybe<Array<Maybe<SiteType>>>;
};

export type RegionTypeSiteArgs = {
  id?: Maybe<Scalars["Float"]>;
  code?: Maybe<Scalars["String"]>;
  code_Icontains?: Maybe<Scalars["String"]>;
  region_Id?: Maybe<Scalars["Float"]>;
  region_Name?: Maybe<Scalars["String"]>;
  region_Name_Icontains?: Maybe<Scalars["String"]>;
  modernName_Icontains?: Maybe<Scalars["String"]>;
  ancientName_Icontains?: Maybe<Scalars["String"]>;
  area_Lt?: Maybe<Scalars["Float"]>;
  area_Gt?: Maybe<Scalars["Float"]>;
};

/** An enumeration. */
export enum SiteFeatureEvidenceEnum {
  /** Very clear evidence */
  A_100 = "A_100",
  /** Clear evidence */
  A_50 = "A_50",
  /** Typical evidence */
  A_0 = "A_0",
  /** Unclear evidence */
  50 = "_50",
  /** Very unclear evidence */
  100 = "_100"
}

export type SiteFeatureType = {
  __typename?: "SiteFeatureType";
  /** How clear is the evidence for the site to have this feature? */
  evidence?: Maybe<SiteFeatureEvidenceEnum>;
  /** feature */
  feature?: Maybe<FeatureType>;
  /** Django object unique identification field */
  id: Scalars["ID"];
  periods?: Maybe<Array<Maybe<PeriodType>>>;
  /** site */
  site?: Maybe<SiteType>;
};

/** An enumeration. */
export enum SiteSurveyTypeEnum {
  /** Surface Survey */
  Surface = "SURFACE",
  /** Excavation */
  Excavation = "EXCAVATION"
}

export type SiteType = {
  __typename?: "SiteType";
  /** Name used by ancient peoples */
  ancientName?: Maybe<Scalars["String"]>;
  /** Area in Hectares. Null is 'unknown' */
  area?: Maybe<Scalars["Float"]>;
  /** Short, meaningful ID for the site. Assigned by the admin */
  code?: Maybe<Scalars["String"]>;
  coordinates: PointFieldType;
  features?: Maybe<Array<Maybe<FeatureType>>>;
  /** Django object unique identification field */
  id: Scalars["ID"];
  /** Name used by modern peoples */
  modernName?: Maybe<Scalars["String"]>;
  /** notes */
  notes?: Maybe<Scalars["String"]>;
  /** value of the original coordinate system of record, if it was easting/northing. Do not use directly */
  notesEastingNorthing?: Maybe<Scalars["String"]>;
  periods?: Maybe<Array<Maybe<PeriodType>>>;
  /** population */
  population?: Maybe<Scalars["Float"]>;
  /** region */
  region?: Maybe<RegionType>;
  sitefeature?: Maybe<Array<Maybe<SiteFeatureType>>>;
  /** survey type */
  surveyType?: Maybe<SiteSurveyTypeEnum>;
};
export type SitesQueryVariables = {
  limit: Scalars["Int"];
};

export type SitesQuery = { __typename?: "Query" } & {
  sites: Maybe<
    Array<
      Maybe<
        { __typename?: "SiteType" } & Pick<
          SiteType,
          "id" | "modernName" | "ancientName"
        > & {
            coordinates: { __typename?: "PointFieldType" } & Pick<
              PointFieldType,
              "x" | "y"
            >;
          }
      >
    >
  >;
};

export const SitesDocument = gql`
  query Sites($limit: Int!) {
    sites(limit: $limit) {
      id
      modernName
      ancientName
      coordinates {
        x
        y
      }
    }
  }
`;
export type SitesComponentProps = Omit<
  ReactApollo.QueryProps<SitesQuery, SitesQueryVariables>,
  "query"
> &
  ({ variables: SitesQueryVariables; skip?: false } | { skip: true });

export const SitesComponent = (props: SitesComponentProps) => (
  <ReactApollo.Query<SitesQuery, SitesQueryVariables>
    query={SitesDocument}
    {...props}
  />
);

export type SitesProps<TChildProps = {}> = Partial<
  ReactApollo.DataProps<SitesQuery, SitesQueryVariables>
> &
  TChildProps;
export function withSites<TProps, TChildProps = {}>(
  operationOptions?: ReactApollo.OperationOption<
    TProps,
    SitesQuery,
    SitesQueryVariables,
    SitesProps<TChildProps>
  >
) {
  return ReactApollo.withQuery<
    TProps,
    SitesQuery,
    SitesQueryVariables,
    SitesProps<TChildProps>
  >(SitesDocument, {
    alias: "withSites",
    ...operationOptions
  });
}

export function useSitesQuery(
  baseOptions?: ReactApolloHooks.QueryHookOptions<SitesQueryVariables>
) {
  return ReactApolloHooks.useQuery<SitesQuery, SitesQueryVariables>(
    SitesDocument,
    baseOptions
  );
}
export type SitesQueryHookResult = ReturnType<typeof useSitesQuery>;
