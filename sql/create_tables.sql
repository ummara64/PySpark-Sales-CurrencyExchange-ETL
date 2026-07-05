CREATE TABLE FactSales
(
    OrderID             VARCHAR(50) PRIMARY KEY,

    ProductID           VARCHAR(50),

    ProductName         VARCHAR(200),

    Category            VARCHAR(100),

    CustomerID          VARCHAR(50),

    Region              VARCHAR(50),

    OrderDate           DATE,

    SaleAmount          DECIMAL(18,2),

    Currency            VARCHAR(10),

    ExchangeRate        DECIMAL(18,6),

    SaleAmountUSD       DECIMAL(18,2),

    Discount            DECIMAL(10,2),

    ConversionTimestamp DATETIME,

    LoadTimestamp       DATETIME DEFAULT GETDATE()
);


-- Rejected Records
CREATE TABLE RejectedRecords
(
    RejectID INT IDENTITY(1,1)
        PRIMARY KEY,

    OrderID VARCHAR(50),

    ProductID VARCHAR(50),

    CustomerID VARCHAR(50),

    RejectReason VARCHAR(200),

    RecordData NVARCHAR(MAX),

    RejectedAt DATETIME DEFAULT GETDATE()
);

-- Currency Conversion log

CREATE TABLE CurrencyConversionLog
(
    ConversionID INT IDENTITY(1,1)
        PRIMARY KEY,

    OrderID VARCHAR(50),

    Currency VARCHAR(10),

    ExchangeRate DECIMAL(18,6),

    SaleAmount DECIMAL(18,2),

    SaleAmountUSD DECIMAL(18,2),

    ConversionTimestamp DATETIME
);

-- Error Log

CREATE TABLE ErrorLog
(
    ErrorID INT IDENTITY(1,1)
        PRIMARY KEY,

    ErrorType VARCHAR(100),

    ErrorMessage NVARCHAR(MAX),

    RecordID VARCHAR(50),

    ErrorTimestamp DATETIME DEFAULT GETDATE()
);