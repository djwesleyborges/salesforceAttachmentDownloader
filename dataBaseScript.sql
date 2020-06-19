USE [SFExtracaoAnexo]
GO

/****** Object:  Table [dbo].[Attachment]    Script Date: 03/06/2020 10:36:39 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO
--drop table Attachment
--select * from Attachment
CREATE TABLE [dbo].[Attachment](
	[Id] [nvarchar](18) NULL,
	[IsDeleted] [bit] NULL,
	[ParentId] [nvarchar](18) NULL,
	[Name] [nvarchar](255) NULL,
	[IsPrivate] [bit] NULL,
	[ContentType] [nvarchar](120) NULL,
	[BodyLength] [int] NULL,
	[Body] [varbinary](max) NULL,
	[OwnerId] [nvarchar](18) NULL,
	[CreatedDate] [nvarchar](50) NULL,
	[CreatedById] [nvarchar](18) NULL,
	[LastModifiedDate] [nvarchar](50) NULL,
	[LastModifiedById] [nvarchar](18) NULL,
	[SystemModstamp] [nvarchar](50) NULL,
	[Description] [nvarchar](500) NULL,
	[ParentType] [nvarchar](500) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO
