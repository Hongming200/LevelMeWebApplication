from flask_wtf import FlaskForm, RecaptchaField
from wtforms import Form, StringField, PasswordField,SelectField, RadioField, SubmitField, TextAreaField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, URL, ValidationError
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import EmailField
import datetime
import re
def only_alp(form, field):
    special_characters = "[@!#$%^&*()<>?/|}{~:]'"
    for char in field.data:
        if char.isdigit():
            raise ValidationError('Make sure there are no numbers.')
        elif char in special_characters:
            raise ValidationError('Make sure there are no special characters')

def only_numbers(form, field):
    for char in field.data:
        if char.isdigit() == False:
            raise ValidationError('Make sure there are only numbers.')
def validate_date(form, field):
    try:
        datetime.datetime.strptime(field.data, '%Y-%m-%d')
    except ValueError:
        raise ValidationError("Incorrect data format, should be YYYY-MM-DD")

def validate_password(form, field):
    SpecialSymbol =['$', '@', '#', '%','!','-','~','.',':','','/']

    if " " in field.data:
        raise ValidationError('Make sure there is no space in between your password.')
    elif not any(char.isupper() for char in field.data):
        raise ValidationError('Password must contain upper case alphabet.')
    elif not any(char.isdigit() for char in field.data):
        raise ValidationError('Password must contain number.')
    elif not any(char in SpecialSymbol for char in field.data):
        raise ValidationError('Password must contain symbol.')

def validate_email(form, field):
    if not (re.fullmatch(r'\b[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', field.data)):
        raise ValidationError("Incorrect Email Format")

class ForgetPasswordForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    submit = SubmitField('Get OTP')

class VerifyOTPForm(FlaskForm):
    email = StringField('OTP',validators=[DataRequired()])
    submit = SubmitField('Verify OTP')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired(),validate_password])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset Password')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired(), Length(min=2, max=20), only_alp])
    last_name = StringField('Last Name',validators=[DataRequired(), Length(min=2, max=20), only_alp])
    email = StringField('Email',validators=[DataRequired(), validate_email])
    password = PasswordField('Password', validators=[DataRequired(), validate_password])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2)])
    recaptcha = RecaptchaField()
    submit = SubmitField('Login')

class UpdatePictureForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Profile Picture')

class UpdateForm(FlaskForm):

    def validate_mobile_phone(form, field):
        if " " in field.data:
            raise ValidationError('Make sure there is no space inbetween your phone numbers.')
        elif field.data.isdigit() == False:
            raise ValidationError('Phone number can only contain numbers.')
        elif len(field.data)<8:
            raise ValidationError('Phone number cannot contain less than 8 numbers.')
        elif len(field.data) > 8:
            raise ValidationError('Phone number cannot contain more than 8 numbers.')

    first_name = StringField('First Name',validators=[DataRequired(), Length(min=2, max=20), only_alp])
    last_name = StringField('Last Name',validators=[DataRequired(), Length(min=2, max=20), only_alp])
    occupation = StringField('Occupation',validators=[DataRequired(), Length(min=2, max=30), only_alp])
    experience = StringField('Work Experience',validators=[DataRequired(), Length(min=2, max=150), only_alp])
    education = StringField('Education',validators=[DataRequired(), Length(min=2, max=150)])
    skills = StringField('Skills',validators=[DataRequired(), Length(min=2, max=150)])
    mobile_phone = StringField('Mobile Phone',validators=[DataRequired(), Length(min=2), validate_mobile_phone])
    email = StringField('Email',validators=[DataRequired(), Email()])
    link = StringField('Classroom Link',validators=[DataRequired(),URL(require_tld=False)])
    social_media = StringField('Social Media',validators=[DataRequired(), Length(min=2, max=150)])
    birthdate = StringField('Birth of Date',validators=[DataRequired(), Length(min=2, max=150), validate_date])
    gender = SelectField('Gender', validators=[DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')])
    language = StringField('Language',validators=[DataRequired(), Length(min=2, max=150), only_alp])
    location = StringField('Location',validators=[DataRequired(), Length(min=2), only_alp])
    submit = SubmitField('Update Profile')


class DeleteAccountForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    submit = SubmitField('Delete Account')


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

class Accept(FlaskForm):
    student = StringField('Students Name',validators=[DataRequired(), Length(min=2, max=150)])
    accept = SubmitField('Accept')

class Delete(FlaskForm):
    student = StringField('Students Name',validators=[DataRequired(), Length(min=2, max=150)])
    delete = SubmitField('Delete')

class IndividualForm(FlaskForm):
    date = StringField('Date',validators=[Length(min=2, max=150), validate_date])
    time = SelectField('TimeSlot',
                           choices=[('0000-0100', '0000-0100'), ('0100-0200', '0100-0200'), ('0200-0300', '0200-0300'),
                                    ('0300-0400', '0300-0400'), ('0400-0500', '0400-0500'), ('0500-0600', '0500-0600'),
                                    ('0600-0700', '0600-0700'), ('0700-0800', '0700-0800'), ('0800-0900', '0800-0900'),
                                    ('0900-1000', '0900-1000'), ('1000-1100', '1000-1100'), ('1100-1200', '1100-1200'),
                                    ('1200-1300', '1200-1300'), ('1300-1400', '1300-1400'), ('1400-1500', '1400-1500'),
                                    ('1500-1600', '1500-1600'), ('1600-1700', '1600-1700'), ('1700-1800', '1700-1800'),
                                    ('1800-1900', '1800-1900'), ('1900-2000', '1900-2000'), ('2000-2100', '2000-2100'),
                                    ('2100-2200', '2100-2200'), ('2200-2300', '2200-2300'), ('2300-2400', '2300-2400')])
    name = StringField('Student Name',validators=[DataRequired(), Length(min=2, max=20), only_alp])
    email = StringField('Email',validators=[DataRequired(), Email()])
    submit = SubmitField('Update individual timeslot')

class UpdateGroupForm(FlaskForm):
    date = StringField('Date', validators=[Length(min=2, max=150), validate_date])
    time = SelectField('TimeSlot',
                           choices=[('0000-0100', '0000-0100'), ('0100-0200', '0100-0200'), ('0200-0300', '0200-0300'),
                                    ('0300-0400', '0300-0400'), ('0400-0500', '0400-0500'), ('0500-0600', '0500-0600'),
                                    ('0600-0700', '0600-0700'), ('0700-0800', '0700-0800'), ('0800-0900', '0800-0900'),
                                    ('0900-1000', '0900-1000'), ('1000-1100', '1000-1100'), ('1100-1200', '1100-1200'),
                                    ('1200-1300', '1200-1300'), ('1300-1400', '1300-1400'), ('1400-1500', '1400-1500'),
                                    ('1500-1600', '1500-1600'), ('1600-1700', '1600-1700'), ('1700-1800', '1700-1800'),
                                    ('1800-1900', '1800-1900'), ('1900-2000', '1900-2000'), ('2000-2100', '2000-2100'),
                                    ('2100-2200', '2100-2200'), ('2200-2300', '2200-2300'), ('2300-2400', '2300-2400')])
    group_no = StringField('Group Number',validators=[DataRequired(), Length(min=1, max=2), only_numbers])
    submit = SubmitField('Update group timeslot')


class DeleteTimeTableForm(FlaskForm):
    choice = SelectField('Individual or Group', choices=[('Individual', 'Individual'), ('Group', 'Group')])
    time = SelectField('TimeSlot',
                           choices=[('0000-0100', '0000-0100'), ('0100-0200', '0100-0200'), ('0200-0300', '0200-0300'),
                                    ('0300-0400', '0300-0400'), ('0400-0500', '0400-0500'), ('0500-0600', '0500-0600'),
                                    ('0600-0700', '0600-0700'), ('0700-0800', '0700-0800'), ('0800-0900', '0800-0900'),
                                    ('0900-1000', '0900-1000'), ('1000-1100', '1000-1100'), ('1100-1200', '1100-1200'),
                                    ('1200-1300', '1200-1300'), ('1300-1400', '1300-1400'), ('1400-1500', '1400-1500'),
                                    ('1500-1600', '1500-1600'), ('1600-1700', '1600-1700'), ('1700-1800', '1700-1800'),
                                    ('1800-1900', '1800-1900'), ('1900-2000', '1900-2000'), ('2000-2100', '2000-2100'),
                                    ('2100-2200', '2100-2200'), ('2200-2300', '2200-2300'), ('2300-2400', '2300-2400')])
    submit = SubmitField('Delete timeslot')

class ContactUsForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    issue = SelectField('Issue', choices=[('Account Management', 'Account Management'), ('Updating Students', 'Updating Students'), ('Updating Timetable', 'Updating Timetable'), ('Others', 'Others')])
    feedback = TextAreaField('Feedback',validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Send Feedback')

class DeleteOnlyForm(FlaskForm):
    delete = SubmitField('Delete')

class ResolvedForm(FlaskForm):
    submit = SubmitField('Issue is Resolved')

class UpdateTicket(FlaskForm):
    choice = SelectField('What do you want to update?', choices=[('Issue', 'Issue'), ('Feedback', 'Feedback')])
    update = TextAreaField('Update to', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Update Support Ticket')

class RetrieveTicket(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    issue = SelectField('Issue', choices=[('Account Management', 'Account Management'), ('Updating Students', 'Updating Students'), ('Updating Timetable', 'Updating Timetable'), ('Others', 'Others')])
    feedback = TextAreaField('Feedback',validators=[DataRequired(), Length(max=200)])


class ReviewForm(FlaskForm):
    rating = SelectField('Give your rating', choices=[('Very Bad', 'Very Bad'), ('Average', 'Average'), ('Very Good', 'Very Good')])
    review = TextAreaField('Review', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Send Review')

class UpdateReviewForm(FlaskForm):
    review = TextAreaField('Review', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Update Review')

class FeedbackForm(Form):
    firstName = StringField('Name',validators=[DataRequired(), Length(min=2, max=150), only_alp])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    type = RadioField('Type of Feedback', choices=[('G', 'Complain'), ('B', 'Compliment')], default='G',render_kw={'style':'margin:5px'})
    remarks = TextAreaField('Feedback', [validators.DataRequired()])
    category = SelectField('Category', [validators.DataRequired()],
                           choices=[('', 'Select'), ('F', 'Teacher'), ('U', 'User'), ('S', 'Service')], default='')
    status = SelectField('Status', [validators.DataRequired()],
                           choices=[('P', 'Pending'), ('R', 'Resolved')], default='P')
    # Name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    # Email = StringField('Email', [validators.Length(min=1, max=150), validators.DataRequired()])
    # cat = SelectField('Category', [validators.DataRequired()], choices=[('', 'Select'), ('', 'Food'), ('', 'User'), ('', 'Service')], default='')
    # remarks = TextAreaField('Feedback', [validators.optional()])
class UpdateFeedbackForm(Form):
    firstName = StringField('Name', [validators.Length(min=1, max=150), validators.optional()])
    email = EmailField('Email', [validators.Email(), validators.optional()])
    type = RadioField('Type of Feedback', choices=[('G', 'Complain'), ('B', 'Compliment')], default='G',render_kw={'style':'margin:5px'})
    remarks = TextAreaField('Feedback', [validators.optional()])
    category = SelectField('Category', [validators.optional()],
                           choices=[('', 'Select'), ('F', 'Teacher'), ('U', 'User'), ('S', 'Service')], default='')
    status = SelectField('Status', [validators.DataRequired()],
                           choices=[('P', 'Pending'), ('R', 'Resolved')], default='P')

class feedbackfilter(Form):
    filter = SelectField('Filter', choices=[('', 'Select'), ('Pending', 'Pending'), ('Resolved', 'Resolved')], default='')

class CreateTaskFormCS(Form):
    urgency = SelectField('Urgency', [validators.DataRequired()], choices=[('', 'Select'), ('U', 'Urgent'), ('N', 'Not Urgent')], default='')
    remarks = TextAreaField('Remarks', [validators.Optional()])

class taskfiltercs(Form):
    filter = SelectField('Filter', choices=[('', 'Select'), ('Urgent', 'Urgent'), ('Not Urgent', 'Not Urgent')], default='')

class CreateProfileCS(Form):
    first_name = StringField('First Name', validators=[Length(min=1, max=150), validators.DataRequired(), only_alp])
    last_name = StringField('Last Name', validators=[Length(min=1, max=150), validators.DataRequired(), only_alp])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    category = SelectField('Membership', [validators.DataRequired()], choices=[('Customer Service', 'Customer Service'), ('Technical Staff', 'Technical Staff'), ('Others', 'Others')], default='Others')
    remarks = TextAreaField('Remarks', [validators.Optional()])

class MessageTCS(Form):
    name = StringField('Name', validators=[Length(min=1, max=150), validators.DataRequired(), only_alp])
    message = TextAreaField('Message', [validators.DataRequired()])
#ayaka end

#justin start

class CreateUserProfileForm(Form):
    first_name = StringField('First Name', validators=[Length(min=1, max=150), validators.DataRequired(), only_alp])
    last_name = StringField('Last Name', validators=[Length(min=1, max=150), validators.DataRequired(), only_alp])
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = StringField('Email',validators=[DataRequired(), Email(), validators.Email()])
    certificates = TextAreaField('Certification', [validators.Optional()])


class CreateUserInterestForm(Form):
    fav = SelectField('Most Interested module',
                      choices=[('M', 'Math'), ('E', 'English'), ('C', 'Chinese'), ('S', 'Science'),
                               ('H', 'History'),
                               ('P', 'POA'), ('G', 'Geography')], default='F')
    hate = SelectField('Least Interested module',
                       choices=[('M', 'Math'), ('E', 'English'), ('C', 'Chinese'), ('S', 'Science'), ('H', 'History'),
                                ('P', 'POA'), ('G', 'Geography')], default='F')


class CreateStudentRequestForm(Form):
    first_name = StringField('First Name', validators=[Length(min=1, max=150), validators.DataRequired(), only_alp])
    last_name = StringField('Last Name', validators=[Length(min=1, max=150), validators.DataRequired(), only_alp])
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = StringField('Email', [validators.Length(min=1, max=150), validators.DataRequired(), validators.Email()])
    size = SelectField("Group/Individual",
                       choices=[('G', 'Group'), ('I', 'Individual')], default='F')
    day = SelectField("Days available",
                      choices=[('Mon', 'Monday'), ('Tues', 'Tuesday'), ('Wed', 'Wednesday'), ('Thurs', 'Thursday'),
                               ('Fri', 'Friday'), ('Sat', 'Saturday'), ('Sun', 'Sunday')])
    timeslot = SelectField('TimeSlot',
                           choices=[('0000-0100', '0000-0100'), ('0100-0200', '0100-0200'), ('0200-0300', '0200-0300'),
                                    ('0300-0400', '0300-0400'), ('0400-0500', '0400-0500'), ('0500-0600', '0500-0600'),
                                    ('0600-0700', '0600-0700'), ('0700-0800', '0700-0800'), ('0800-0900', '0800-0900'),
                                    ('0900-1000', '0900-1000'), ('1000-1100', '1000-1100'), ('1100-1200', '1100-1200'),
                                    ('1200-1300', '1200-1300'), ('1300-1400', '1300-1400'), ('1400-1500', '1400-1500'),
                                    ('1500-1600', '1500-1600'), ('1600-1700', '1600-1700'), ('1700-1800', '1700-1800'),
                                    ('1800-1900', '1800-1900'), ('1900-2000', '1900-2000'), ('2000-2100', '2000-2100'),
                                    ('2100-2200', '2100-2200'), ('2200-2300', '2200-2300'), ('2300-2400', '2300-2400')])

#justin end



class CreateUserForm(Form):
    first_name = StringField('First Name', validators=[Length(min=1, max=150), validators.DataRequired(), only_alp])
    last_name = StringField('Last Name', validators=[Length(min=1, max=150), validators.DataRequired(), only_alp])
    email = StringField('Email', [validators.Email(),validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    role = RadioField('Role', choices=[('C', 'Customer Service'), ('NE', 'Network Engineer'), ('S', 'Software Developer')], default='C')
    remarks = TextAreaField('Remarks', [validators.Optional()])

class CreateAdminFormTask(Form):
    task = StringField('Tasks', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={'style':'width:800px;font-size:30px'})
    done_by = StringField('Done By', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={'style':'width:500px;font-size:20px'})

class CreateAdminProfile(Form):
    company = StringField('Company', [validators.Length(min=1, max=150)] )
    username = StringField('Username', [validators.Length(min=1, max=150)] )
    admin_email = StringField('Admin Email', [validators.Email(),validators.Length(min=1, max=150)])
    admin_first_name = StringField('First Name', validators=[Length(min=1, max=150), only_alp])
    admin_last_name = StringField('Last Name', validators=[Length(min=1, max=150), only_alp])
    address = StringField('Address', [validators.Length(min=1, max=150)])
    city = StringField('City', [validators.Length(min=1, max=150)])
    country = StringField('Country', [validators.Length(min=1, max=150)])
    postal_code = StringField('Postal Code', [validators.Length(min=1, max=150)])

class CreateStaffMessage(Form):
    message_name = StringField('Name', validators=[Length(min=1, max=150), validators.DataRequired(), only_alp], render_kw={'style':'width:200px;font-size:15px'})
    message_email = StringField('Email', [validators.Email(),validators.Length(min=1, max=150), validators.DataRequired()], render_kw={'style':'width:300px;font-size:15px'})
    message = StringField('Message', [validators.Length(min=1, max=150), validators.DataRequired()], render_kw={'style':'width:600px;font-size:15px'})

class EmailSubscription(Form):
    recaptcha = RecaptchaField()
    emailsubscription_name = StringField('Name',validators=[DataRequired(), Length(min=2, max=180), only_alp], render_kw={'style':'width:400px;font-size:15px;'})
    emailsubscription_email = EmailField('Email', [validators.Email(), validators.Length(min=1, max=150), validators.DataRequired()], render_kw={'style':'width:500px;font-size:15px;'})

class AuthenticationForm(FlaskForm):
    otp = StringField('OTP', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Confirm OTP')
