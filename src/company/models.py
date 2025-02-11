from datetime import date

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    Date,
    Boolean,
    text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Employee(Base):
    """Model employee."""

    first_name: Mapped[str] = mapped_column(
        String(150),
        CheckConstraint(
            "0 < LENGTH(first_name) <= 150", name="check_len_first_name"
        ),
        unique=True,
        nullable=False,
        comment=(
            "Имя сотрудника, обязательное строковое поле;"
            " Допустимая длина строки — от 1 до 150 символов включительно;"
        ),
    )
    last_name: Mapped[str] = mapped_column(
        String(150),
        CheckConstraint(
            "0 < LENGTH(last_name) <= 150", name="check_len_last_name"
        ),
        unique=True,
        nullable=False,
        comment=(
            "Фамилия сотрудника, обязательное строковое поле;"
            " Допустимая длина строки — от 1 до 150 символов включительно;"
        ),
    )
    middle_name: Mapped[str] = mapped_column(
        String(150),
        CheckConstraint(
            "0 < LENGTH(middle_name) <= 150", name="check_len_middle_name"
        ),
        unique=True,
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
        comment="Дата и время устройства сотрудника.",
    )
    termination_date: Mapped[date] = mapped_column(
        Date,
        nullable=True,
        comment="Дата и время увольнения сотрудника."
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
        comment=(
            "Зарплата сотрудника, позитивное целочисленное значение."
        )
    )

    # relation fields
    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("employee.id"),
        CheckConstraint("id != manager_id", name="not_equal_id_or_manager_id"),
        nullable=True
    )
    manager: Mapped["Employee"] = relationship(back_populates="subordinates")
    subordinates: Mapped[list["Employee"]] = relationship(
        back_populates="manager"
    )

    division_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("Division.id"),
        nullable=True
    )
    division: Mapped["Division"] = relationship(back_populates="employees")

    position_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Division.id"),
        nullable=False
    )
    position: Mapped["Position"] = relationship(
        back_populates="employees",
        cascade="all, delete"
    )

    status_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Division.id"),
        nullable=False
    )
    status: Mapped["Status"] = relationship(
        back_populates="employees",
        cascade="all, delete"
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
        )
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.id}"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.id}, {self.name}"


class Division(BaseModel):
    """Division model."""

    __table_args__ = (
        CheckConstraint(
            "0 < LENGTH(name) <= 150",
            name='check_len_division_name'
        ),
    )

    # relation fields
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("division.id")
    )
    parent: Mapped["Division"] = relationship(back_populates="child")
    child: Mapped[list["Division"]] = relationship(back_populates="parent")

    employees: Mapped[list[Employee]] = relationship(back_populates="division")


class Position(BaseModel):
    """Position model."""

    __table_args__ = (
        CheckConstraint(
            "0 < LENGTH(name) <= 150",
            name='check_len_position_name'
        ),
    )

    employees: Mapped[list[Employee]] = relationship(back_populates="position")


class Status(BaseModel):
    """Status model."""

    __table_args__ = (
        CheckConstraint(
            "0 < LENGTH(name) <= 150",
            name='check_len_status_name'
        ),
    )

    employees: Mapped[list[Employee]] = relationship(back_populates="status")
