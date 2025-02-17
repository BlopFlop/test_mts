from datetime import date

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Employee(Base):
    """Model employee."""

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment="Номер в базе данных",
    )
    first_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        comment=(
            "Имя сотрудника, обязательное строковое поле;"
            " Допустимая длина строки — от 1 до 150 символов включительно;"
        ),
    )
    last_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        comment=(
            "Фамилия сотрудника, обязательное строковое поле;"
            " Допустимая длина строки — от 1 до 150 символов включительно;"
        ),
    )
    middle_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        comment=(
            "Отчество сотрудника, обязательное строковое поле;"
            " Допустимая длина строки — от 1 до 150 символов включительно;"
        ),
    )

    hire_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        default=date.today(),
        comment="Дата устройства сотрудника.",
    )
    termination_date: Mapped[date] = mapped_column(
        Date, nullable=True, comment="Дата увольнения сотрудника."
    )

    is_staff: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true"),
        nullable=False,
        comment=(
            "Булево значение, определяющее штатного сотрудника."
            "True, штатный. False, Внештатный сотрудник."
        ),
    )
    salary: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("0 < salary", name="check_positive_salary"),
        default=0,
        nullable=False,
        comment=("Зарплата сотрудника, позитивное целочисленное значение."),
    )

    __table_args__ = (
        CheckConstraint("salary > 0", name="check_positive_salary"),
        CheckConstraint(
            "LENGTH(first_name) > 0", name="check_not_null_first_name"
        ),
        CheckConstraint(
            "LENGTH(last_name) > 0", name="check_not_null_last_name"
        ),
        CheckConstraint(
            "LENGTH(middle_name) > 0", name="check_not_null_middle_name"
        ),
        UniqueConstraint("id", "manager_id", name="employee_uniq_pk_to_fk"),
    )

    # relation fields
    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("employee.id"),
        CheckConstraint("id != manager_id", name="not_equal_id_or_manager_id"),
        nullable=True,
    )
    manager: Mapped["Employee"] = relationship(
        "Employee", back_populates="subordinates", remote_side=[id]
    )
    subordinates: Mapped[list["Employee"]] = relationship(
        "Employee", back_populates="manager", remote_side=[manager_id]
    )

    division_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("division.id"), nullable=True
    )
    division: Mapped["Division"] = relationship(back_populates="employees")

    position_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("position.id"), nullable=False
    )
    position: Mapped["Position"] = relationship(
        back_populates="employees", cascade="all, delete"
    )

    status_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("status.id"), nullable=False
    )
    status: Mapped["Status"] = relationship(
        back_populates="employees", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.id}"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.id}, {self.first_name}"


class BaseModel(Base):
    __abstract__ = True

    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        comment=(
            "Уникальное имя, обязательное строковое поле;"
            " Допустимая длина строки от 1 до 150 символов влкючительно."
        ),
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.id}"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.id}, {self.name}"


class Division(BaseModel):
    """Division model."""

    __table_args__ = (
        CheckConstraint(
            "LENGTH(name) > 0", name="check_not_null_division_name"
        ),
        UniqueConstraint("id", "parent_id", name="division_uniq_pk_to_fk"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment="Номер в базе данных",
    )

    # relation fields
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("division.id"))
    parent: Mapped["Division"] = relationship(
        back_populates="child", remote_side=[id]
    )
    child: Mapped[list["Division"]] = relationship(
        back_populates="parent", remote_side=[parent_id]
    )

    employees: Mapped[list[Employee]] = relationship(back_populates="division")


class Position(BaseModel):
    """Position model."""

    __table_args__ = (
        CheckConstraint(
            "LENGTH(name) > 0", name="check_not_null_position_name"
        ),
    )

    employees: Mapped[list[Employee]] = relationship(back_populates="position")


class Status(BaseModel):
    """Status model."""

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="check_not_null_status_name"),
    )

    employees: Mapped[list[Employee]] = relationship(back_populates="status")
