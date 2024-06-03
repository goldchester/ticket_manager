DROP TABLE IF EXISTS tickets;
CREATE TABLE IF NOT EXISTS "tickets" (
	"id" bigint GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
	"title" varchar(100) NOT NULL,
	"created_by_id" smallint NOT NULL,
	"assigned_to_dep" smallint NOT NULL,
	"assigned_to" smallint,
	"created_at" timestamp with time zone NOT NULL DEFAULT now(),
	"problem" varchar(1000) NOT NULL,
	"priority_id" smallint NOT NULL,
	"status_id" smallint NOT NULL,
	"solved_at" timestamp with time zone,
	"solutions" varchar(1000),
	PRIMARY KEY ("id")
);

DROP TABLE IF EXISTS employees;
CREATE TABLE IF NOT EXISTS "employees" (
	"id" bigint GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
	"name" varchar(50) NOT NULL,
	"surname" varchar(50) NOT NULL,
	"dep" smallint NOT NULL,
	PRIMARY KEY ("id")
);

DROP TABLE IF EXISTS departments;
CREATE TABLE IF NOT EXISTS "departments" (
	"id" bigint GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
	"name" varchar(50) NOT NULL,
	PRIMARY KEY ("id")
);

DROP TABLE IF EXISTS priority;
CREATE TABLE IF NOT EXISTS "priority" (
	"id" bigint GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
	"name" varchar(20) NOT NULL,
	PRIMARY KEY ("id")
);

DROP TABLE IF EXISTS status;
CREATE TABLE IF NOT EXISTS "status" (
	"id" bigint GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
	"name" varchar(20) NOT NULL,
	PRIMARY KEY ("id")
);

ALTER TABLE "employees" ADD CONSTRAINT "employees_fk3" FOREIGN KEY ("dep") REFERENCES "departments"("id");
ALTER TABLE "tickets" ADD CONSTRAINT "tickets_fk2" FOREIGN KEY ("created_by_id") REFERENCES "employees"("id");

ALTER TABLE "tickets" ADD CONSTRAINT "tickets_fk3" FOREIGN KEY ("assigned_to_dep") REFERENCES "departments"("id");

ALTER TABLE "tickets" ADD CONSTRAINT "tickets_fk4" FOREIGN KEY ("assigned_to") REFERENCES "employees"("id");

ALTER TABLE "tickets" ADD CONSTRAINT "tickets_fk7" FOREIGN KEY ("priority_id") REFERENCES "priority"("id");

ALTER TABLE "tickets" ADD CONSTRAINT "tickets_fk8" FOREIGN KEY ("status_id") REFERENCES "status"("id");