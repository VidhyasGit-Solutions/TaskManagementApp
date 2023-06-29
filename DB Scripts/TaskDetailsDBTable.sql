USE TaskManagementDB;
GO
/*==============================================================*/
/* Table: taskdetails                                              */
/*==============================================================*/
CREATE TABLE [dbo].[taskdetails] (
    [taskId]  		INT           IDENTITY(1,1),
	[UserId]   		INT			  NOT NULL,
    [name]   		VARCHAR (255) NOT NULL,
    [description]   VARCHAR (255) NULL,
	[priority]   	VARCHAR (255) NULL,
	[category]   	VARCHAR (255) NULL,
    [status]      	VARCHAR (100) NOT NULL,
    [duedate] 		DATETIME      NOT NULL,
    CONSTRAINT [PK_TASKDETAILS] PRIMARY KEY CLUSTERED ([taskId] ASC),
	FOREIGN KEY (UserId) REFERENCES useraccounts(Id)
);
