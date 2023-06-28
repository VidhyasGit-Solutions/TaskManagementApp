USE TaskManagementDB;
GO
/*==============================================================*/
/* Table: useraccounts                                              */
/*==============================================================*/
CREATE TABLE [dbo].[useraccounts] (
    [Id]         INT           IDENTITY(1,1),
    [username]   VARCHAR (50)  NOT NULL,
    [password]   VARCHAR (255) NOT NULL,
    [email]      VARCHAR (100) NOT NULL,
    [created_at] DATETIME      NOT NULL DEFAULT getdate(),
    CONSTRAINT [PK_USERACCOUNTS] PRIMARY KEY CLUSTERED ([Id] ASC)
);
