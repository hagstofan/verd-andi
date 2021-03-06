USE [PPP]
GO
/****** Object:  Table [dbo].[obs_images]    Script Date: 14.10.2020 08:07:19 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[obs_images](
	[image_id] [int] IDENTITY(1,1) NOT NULL,
	[observation_id] [int] NOT NULL,
	[itemcode] [varchar](20) NOT NULL,
	[item_image] [varchar](200) NULL,
 CONSTRAINT [PK_obs_images] PRIMARY KEY CLUSTERED 
(
	[image_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ö_obs$]    Script Date: 14.10.2020 08:07:19 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ö_obs$](
	[observation_PX] [int] NOT NULL,
	[itemcode_i_konnun] [varchar](20) NOT NULL,
	[obs_comments] [varchar](max) NULL,
	[obs_price] [numeric](12, 2) NULL,
	[nr_konnunar] [varchar](12) NULL,
	[status_obs] [char](1) NULL,
	[obs_quantity] [numeric](6, 2) NULL,
	[representative] [varchar](6) NULL,
	[shopid] [varchar](50) NULL,
	[datamonth] [char](2) NULL,
	[discount_flag] [char](1) NULL,
	[shop_type] [varchar](30) NULL,
	[loaded_date] [date] NULL,
	[brand] [varchar](100) NULL,
	[observer] [varchar](100) NULL,
	[picture] [varchar](200) NULL,
	[barcode] [varchar](20) NULL,
 CONSTRAINT [PK_observation ] PRIMARY KEY CLUSTERED 
(
	[observation_PX] ASC,
	[itemcode_i_konnun] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  View [dbo].[vw_observation_picture]    Script Date: 14.10.2020 08:07:19 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
--insert into [dbo].[obs_images]
--select distinct [observation_PX] ,[itemcode_i_konnun],[picture] from [dbo].[ö_obs$]
--where picture is not null

create view [dbo].[vw_observation_picture]
as
SELECT [observation_PX]
      ,[itemcode_i_konnun]
      ,[obs_comments]
      ,[obs_price]
      ,[nr_konnunar]
      ,[status_obs]
      ,[obs_quantity]
      ,[representative]
      ,[shopid]
      ,[datamonth]
      ,[discount_flag]
      ,[shop_type]
      ,[loaded_date]
      ,[brand]
      ,[observer]
	  ,item_image as picture
      ,[barcode]
  FROM [dbo].[ö_obs$] a 
  left join [dbo].[obs_images] b
  on [observation_PX] = [observation_id]
  and [itemcode_i_konnun] = [itemcode]
GO
ALTER TABLE [dbo].[obs_images]  WITH CHECK ADD  CONSTRAINT [FK_ö_obs$_observation_itemcode] FOREIGN KEY([observation_id], [itemcode])
REFERENCES [dbo].[ö_obs$] ([observation_PX], [itemcode_i_konnun])
GO
ALTER TABLE [dbo].[obs_images] CHECK CONSTRAINT [FK_ö_obs$_observation_itemcode]
GO
