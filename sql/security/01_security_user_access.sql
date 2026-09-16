USE WideWorldImportersDW;
GO

-- ============================================================
-- SupplyChain360
-- Optional production RLS mapping table
-- ============================================================
-- The PBIP ships with an in-model demo Security User Access table
-- so the project opens without extra setup.
--
-- In a production deployment, replace the demo mapping with a
-- governed table such as the one below.
-- NEVER commit real production user mappings to a public repo.
-- ============================================================

IF SCHEMA_ID('security') IS NULL
    EXEC('CREATE SCHEMA security');
GO

IF OBJECT_ID('security.UserRegionAccess', 'U') IS NULL
BEGIN
    CREATE TABLE security.UserRegionAccess
    (
        UserPrincipalName nvarchar(320) NOT NULL,
        StateProvince     nvarchar(100) NOT NULL,
        AccessLevel       nvarchar(50)  NOT NULL
            CONSTRAINT DF_UserRegionAccess_AccessLevel
            DEFAULT ('Regional Manager'),
        IsActive          bit NOT NULL
            CONSTRAINT DF_UserRegionAccess_IsActive
            DEFAULT (1),
        EffectiveFrom     date NULL,
        EffectiveTo       date NULL,

        CONSTRAINT PK_UserRegionAccess
            PRIMARY KEY (UserPrincipalName, StateProvince)
    );
END;
GO

-- Example only:
-- INSERT INTO security.UserRegionAccess
--     (UserPrincipalName, StateProvince, AccessLevel)
-- VALUES
--     ('manager@company.com', 'Texas', 'Regional Manager');

SELECT
    UserPrincipalName,
    StateProvince,
    AccessLevel,
    IsActive,
    EffectiveFrom,
    EffectiveTo
FROM security.UserRegionAccess
ORDER BY UserPrincipalName, StateProvince;
GO
